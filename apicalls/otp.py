from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from datetime import datetime,timezone,timedelta
from django.contrib.auth.models import User
import logging
from libraries.ip_fetch import ipfetch
from libraries.new_request import CreateRequestStatus
from constants.otp_variables import OTP_EXP_TIME,OTP_LENGTH,OTPSTR,REQUESTTOKSTR
import string
import random
import requests
import hashlib
from rest_framework.authtoken.models import Token
from exam.models import (ExamServerOTP,ExamCenter,ExamMember,CenterCiMapping,
                         CenterDeviceMapping,ExamDevice,CenterSlotMapping,ExamSlot,
                         ExamDetails)
from libraries.validate_exception import validateexamceter

api_ilogger = logging.getLogger('api_log')
api_elogger = logging.getLogger('api_error')


class SendSMS:

    def calculatehashval(self, val1, val2, val3,val4):
        m = hashlib.sha512()
        tohash = "".join([val1.strip(), val2.strip(), val3.strip(), val4.strip()])
        m.update(tohash.encode())
        return m.hexdigest()
    
    def sendsms(self, otp, mobile,centercode):
        url = "https://msdgweb.mgov.gov.in/esms/sendsmsrequestDLT"
        rdata = dict()
       
        senmessage = f"Dear CI, The OTP to authenticate in PXE server for center {centercode} is : {otp} .This is valid for {OTP_EXP_TIME} mins - CDAC"

        rdata["username"] = "VMCDAC"
        rdata["password"] = "abcd1234!@#"
        rdata["content"] = senmessage
        rdata["senderid"] = "FPCDAC"
        rdata["mobileno"] = str(mobile)
        rdata["key"] = self.calculatehashval("VMCDAC","FPCDAC",senmessage,"56f801cc-8ed0-4bd2-b2b5-f652dbc4a8e9")
        rdata["templateid"] = "1307164265672479174"
        rdata["smsservicetype"] = "singlemsg"
        
        # print(rdata)

        sendsinglesms = requests.post(url, data=rdata)
        # print(sendsinglesms)
        try:
            api_id = str(sendsinglesms.text).split('=')[1].strip()
        except Exception :
            api_id = ''
        
        ExamServerOTP.objects.filter(otp = otp).update(otp_api_id = api_id, contact_number = mobile)
        return sendsinglesms.status_code


class ExamOTP:
    def __init__(self,lengthn):
            self.nlen = lengthn

    def generate_otp(self,nlen,examcode):
        '''To generate OTP of length nlen with digits only'''
        only_digits = string.digits
        while True:
            otp = ''.join(random.sample(only_digits,nlen))
            full_otp = str(examcode.id)+"-"+str(otp)
            try:
                # print("The OTP is",full_otp)
                ifexist = ExamServerOTP.objects.get(otp=full_otp,examcode=examcode)
                # print("opt {0} already exist".format(full_otp))
                continue
            except Exception as details:
                api_elogger.error("%s"%(details))
                return full_otp

    def is_active(self,center_code,examcode):
        '''To check if there is already a active OTP'''
        curr_time = datetime.now(timezone.utc)
        b4_5_mins = curr_time - timedelta(minutes = 5)
        otp_list = ExamServerOTP.objects.filter(status="active",expiry__lte=b4_5_mins,user_center=center_code,examcode=examcode).values_list('otp',flat=True)
        for otp in otp_list:
                try:
                        otp_rec = ExamServerOTP.objects.get(otp=otp,user_center=center_code,examcode=examcode)
                        otp_rec.status = "expired"
                        otp_rec.save()
                except Exception as details:
                        api_elogger.info('Unable to get OTP record '+str(details))
                        print("Unable to get OTP record"+str(details))
        try:
                active_rec = ExamServerOTP.objects.get(user_center=center_code,examcode=examcode,status="active")
                if active_rec:
                        return active_rec.otp
        except ExamServerOTP.DoesNotExist as otpexp:
                api_elogger.info("Error while trying to get Active OTP record: "+str(otpexp))
                print("Error while trying to get OTP record: "+str(otpexp))
                api_elogger.error("Error while trying to get OTP record: "+str(otpexp))
                return False
        return False
        
class PXEOTPGEN(ObtainAuthToken):
    def post(self,request):
        mobile = request.data['mobile']
        center_code = request.data['username']
        password = request.data['password']
        reqtime = request.data['reqtime']
        exam_code = request.data['exam_code']
        devicename = request.data['devicename']

        # print(mobile, center_code, password,reqtime)
        user = authenticate(username=center_code,password=password)
        if not user:
            return Response({'status': 0, 'msg' : "Login Authentication Failed"})
        try:
            examdetob = ExamDetails.objects.get(examcode=exam_code,isactive=True)
            cenobj = ExamCenter.objects.get(centercode = center_code,examcode=examdetob)
            devobj = ExamDevice.objects.get(device_name=devicename,is_mapped=1)
            devmapp = CenterDeviceMapping.objects.get(examcode=examdetob,centercode=cenobj,examdevice=devobj,islive=1)
            member = ExamMember.objects.get(contact_number = mobile, memberrole__roletype = 'CI')
            centcimapp = CenterCiMapping.objects.get(centercode = cenobj, membername = member,examcode=examdetob)
            slotmapp = CenterSlotMapping.objects.filter(centercode = cenobj,examcode=examdetob).values('examslot')
            slots = ExamSlot.objects.filter(pk__in = slotmapp, download_time__date = datetime.today())

            if not slots.exists():
                raise ExamSlot.DoesNotExist
            
            ip = ipfetch(request)
            cotp = ExamOTP(OTP_LENGTH)
            
        except ExamDetails.DoesNotExist:
            return Response({'api_status': 0, 'msg' : "No active exam is scheduled"})
        except ExamCenter.DoesNotExist:
            return Response({'api_status': 0, 'msg' : "Invalid Center Code"})
        except (ExamDevice.DoesNotExist, CenterDeviceMapping.DoesNotExist):
            return Response({'api_status': 0, 'msg' : "Exam Device is not mapped for Exam"})
        except ExamMember.DoesNotExist:
            return Response({'api_status': 0, 'msg' : "Enter Valid Mobile Number of CI"})
        except CenterCiMapping.DoesNotExist:
            return Response({'api_status': 0, 'msg' : "Mobile Number / Center Code Mismatch"})
        except ExamSlot.DoesNotExist:
            return Response({'api_status': 0, 'msg' : "No Slots Available for this Exam Center on Today"})
        except Exception as error:
            print("Exception in pxe request details: " + error)
            api_elogger.error("Exception in pxe request details: %s" % (error))
            return Response({'api_status': 0, 'msg' : "Unable Generate OTP"})
        else:
            userobj = User.objects.get(username=center_code)
            old_otp = cotp.is_active(userobj,examdetob)
            
            if old_otp:
                smsobj = SendSMS()
                smsobj.sendsms(old_otp, member.contact_number,center_code)
                CreateRequestStatus(examcode=examdetob,centercode=cenobj,request_type=OTPSTR,request_priority="HIGH",ipaddress=ip,requesttime=reqtime)
                return Response({'status' : 1, 'msg' : "OTP Generated", 'mob' : member.contact_number, 
                                'name' : member.membername, 'task' : OTPSTR})
            
            otp = cotp.generate_otp(cotp.nlen,examdetob)
            curr_time = datetime.now(timezone.utc)
            expiry_time = curr_time + timedelta(minutes=OTP_EXP_TIME)
            try:
                ExamServerOTP.objects.create(examcode=examdetob,otp=otp,user_center=userobj,status="active",expiry=expiry_time,contact_number=member.contact_number,otp_type="PXEOTP",record_created_by=userobj)
                smsobj = SendSMS()
                x = smsobj.sendsms(otp, member.contact_number,center_code)
                if x == 200:
                    CreateRequestStatus(examcode=examdetob,centercode=cenobj,request_type=OTPSTR,request_priority="HIGH",ipaddress=ip,requesttime=reqtime)
                    return Response({'status' : 1, 'msg' : "OTP Generated", 'mob' : member.contact_number, 'name' : member.membername, 'task' : OTPSTR})
                else:
                    return Response({'status' : 0, 'msg' : "Unable to Send OTP"})
                
            except Exception as otpsave:
                print("Except in OTP save "+str(otpsave))
                api_elogger.error("Error sending OTP %s",otpsave)
                return Response({'status':0, 'msg' : "Unable Generate OTP"})



class CustomAuthToken(ObtainAuthToken):

    def validateOTP(self,exam_code,centercode, otp):
        try:
            otpobj = ExamServerOTP.objects.get(examcode=exam_code,user_center=centercode,otp=otp,status='active')

            if datetime.now(timezone.utc) < otpobj.expiry:
                # otpobj.status = "used"
                # otpobj.save()
                return True
            else:
                otpobj.status = "expired"
                otpobj.save()
                return False
        except Exception as details:
            print(details,"No Valid OTP Found")
            api_elogger.error("%s" % (details))
            return False

    def post(self, request):
        try:
            exam_code = request.data['exam_code']
            centercode = request.data['username']
            password = request.data['password']
            user = authenticate(username=centercode, password=password)
            if not user:
                content  = {'status' : "0", 'Message' : "Login Authentication Failed"}
                return Response(content)

            otpval = request.data['otp']
            
            validatecenter = validateexamceter(exam_code,centercode)
            if not validatecenter['status']:
                content  = {'status' : "0", 'Message' : validatecenter['message']}
                return Response(content)
            
            examobject = validatecenter['examobject']
            centerobj = validatecenter['centerobj']
            userobj = User.objects.get(username=centerobj.centercode)

            validateotp = self.validateOTP(examobject,userobj,otpval)

            if not validateotp:
                content  = {'status' : "0", 'Message' : "Invalid OTP / Center Code"}
                return Response(content)
            
            slotmapp = CenterSlotMapping.objects.filter(examcode= examobject,centercode = centerobj).values('examslot')
            slots = ExamSlot.objects.filter(pk__in = slotmapp, download_time__date = datetime.today())
            
            if not slots.exists():
                raise ExamSlot.DoesNotExist

            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user = user)
                
            try:
                request_type = REQUESTTOKSTR
                ip = ipfetch(request)
                reqtime = request.data['reqtime']

                CreateRequestStatus(examcode=examobject,centercode=centerobj,
                                    request_type=request_type,request_priority="HIGH",
                                    ipaddress=ip,requesttime=reqtime)
                otpobj = ExamServerOTP.objects.filter(examcode=examobject,user_center = userobj).latest('record_created_at')
                otpobj.used = datetime.now()
                otpobj.save()
                
            except Exception as details:
                print("issue in updating status table",details)
                api_elogger.error(details)

            center_name = centerobj.centername
            city_name = centerobj.examcity.cityname

            try:
                cimappig = CenterCiMapping.objects.get(centercode = centerobj,examcode=examobject)
            except Exception:
                cimappig = CenterCiMapping.objects.filter(centercode = centerobj,examcode=examobject)[0]

            respose_data = {"token": token.key, "ciname" : cimappig.membername.membername, "mob":cimappig.membername.contact_number,
                            "centername" : center_name,"cityname" : city_name }
           
            return Response(respose_data)
       
        except ExamSlot.DoesNotExist:
            return Response({'api_status': 0, 'msg' : "No Slots Available for this Exam Center on Today"})
        except ExamCenter.DoesNotExist:
            return Response({'api_status' : 0, 'msg' : "Invalid Center Code / OTP"})
        except Exception as details:
            print(details)
            content = dict()
            content['status'] = 0
            content['msg'] = "Incorrect request"
            api_elogger.error("%s" % (details))
            return Response(content)
