from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from . models import *                          
from .serializers import *
from utils.choices import center_status,center_rating
object_not_exist = []

# function to get primary key
def get_pk(model, filter_fields):
    try:
        response = model.objects.filter(**filter_fields).first()
        if response:
            response_id = response.pk
            return response_id
        else :
            raise ObjectDoesNotExist(f"{filter_fields} Not found")
    except Exception as e:
        # print("Exception in name_id_convertor fun",str(e))
        return False
    
# Exam Details API's 
class ExamDetailView(APIView):
    """
    API View to handle the creation of ExamDetails records.

    This view processes POST requests containing exam detail information in JSON format.
    It expects the following fields in the request body:

    - examname: The name of the exam.
    - client_name: The name of the client associated with the exam.
    - no_of_examdays: The number of days allocated for the exam.
    - no_of_examslot: The number of exam slots available.
    - no_of_centers: The number of centers where the exam will be conducted.
    - exam_startdate: The start date of the exam in DD-MM-YYYY format.
    - exam_enddate: The end date of the exam in DD-MM-YYYY format.
    - mock_startdate: The start date for the mock exam in DD-MM-YYYY format.
    - mock_enddate: The end date for the mock exam in DD-MM-YYYY format.
    - exam_hash: A unique hash for the exam. 
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)

            
            check_existance = ExamDetails.objects.filter(examcode = data['examcode'])
            if check_existance:
                return Response({"api_status": False, "message": f"examcode {data['examcode']} Already Exist"})
            else:
                serliazer = ExamDetailSerializer(data=data)
                if serliazer.is_valid():
                    serliazer.save()
                    return Response({"api_status": True, "message": "Exam Detail's Data Saved Successfully"})
                else:
                    return Response({"api_status": False, "message": "Invalid Input" , "Error":serliazer.errors})
        except Exception as e:
            # print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        

class ExamDetailListView(APIView):
    """
    API View to handle the list of ExamDetails records.
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_details = ExamDetails.objects.all()
            if not exam_details.exists():
                raise ObjectDoesNotExist("Exam Details Data, Not Found")

            serializer = ExamDetailSerializer(exam_details, many=True)
            return Response({"api_status": True, "data": serializer.data})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})

       
class ExamDetailUpdateView(APIView):
    """
    API View to handle the updating of ExamDetails records.

    This view processes POST requests to update existing exam detail records.
    It expects the following fields in the request body:

    - examname: The name of the exam.
    - client_name: The name of the client associated with the exam.
    - no_of_examdays: The number of days allocated for the exam.
    - no_of_examslot: The number of exam slots available.
    - no_of_centers: The number of centers where the exam will be conducted.
    - exam_startdate: The start date of the exam in DD-MM-YYYY format.
    - exam_enddate: The end date of the exam in DD-MM-YYYY format.
    - mock_startdate: The start date for the mock exam in DD-MM-YYYY format.
    - mock_enddate: The end date for the mock exam in DD-MM-YYYY format.
    - exam_hash: A unique hash for the exam.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing ExamDetail record.
        
        :param id: Primary key of the ExamDetail record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_detail = ExamDetails.objects.get(id=id)
            serliazer = ExamDetailSerializer(exam_detail,data=data)

            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except ExamDetails.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamDetailDeleteView(APIView):
    """
    API View to handle the deletion of ExamDetails records.

    This view processes DELETE requests to remove existing exam detail records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles DELETE requests to remove an existing ExamDetail record.
        
        param id: Primary key of the ExamDetails record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_detail = ExamDetails.objects.get(id=id)
            exam_detail.delete()
            return Response({"api_status": True, "message": "Data Deleted Successfully"})

        except ExamDetails.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})

# Exam Slot API's       
class ExamSlotView(APIView):
    """
    API View to handle the creation of Exam Slot records.

    This view processes POST requests containing exam slot information in JSON format.
    It expects the following fields in the request body:

    - slotname: The name of the slot.
    - download_time: To be download Date&Time.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serliazer = ExamSlotSerializer(data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        
class ExamSlotListView(APIView):
    """
    API View to handle the list of Exam Slot's records.

    This view processes POST requests containing exam slot information response in JSON format.
    It return  the following fields in the response body:

    - id : The primary key id 
    - slot_name: The name of the slot.
    - download_time : download time of the slot
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_slot_response = ExamSlot.objects.values('id', 'examslot', 'download_time')
            if not exam_slot_response:
                raise ObjectDoesNotExist("No Data Found")            
            data = list(exam_slot_response)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        

class ExamSlotUpdateView(APIView):
    """
    API View to handle the updating of Exam Slot's records.

    This view processes POST requests to update existing exam slot records.
    It expects the following fields in the request body:

    - id: The id or primary key
    - slot_name: The name of the slot.
    - download_time: The number of days allocated for the exam.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing Exam Slot's record.
        
        :param id: Primary key of the ExamDetail record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_slot = ExamSlot.objects.get(id=id)
            serliazer = ExamSlotSerializer(exam_slot,data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
            
        except ExamSlot.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamSlotDeleteView(APIView):
    """
    API View to handle the deletion of ExamDetails records.

    This view processes DELETE requests to remove existing exam slot records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing Exam Slot record.
        
        param id: Primary key of the exam slot record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_slot = ExamSlot.objects.get(id=id)
            exam_slot.delete()
            return Response({"api_status": True, "message": "Data Deleted Successfully"})
        except ExamSlot.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"},)
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})
        
# Exam Paper's API 
class PaperTypeView(APIView):
    """
    API View to handle the creation of Paper type records.

    This view processes POST requests containing Papertype information in JSON format.
    It expects the following fields in the request body:

    - papertype: The name of the paper.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serliazer = PaperTypeSerializer(data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)},status=status.HTTP_400_BAD_REQUEST)
        
class PaperTypeListView(APIView):
    """
    API View to handle the list of Papertype's records.

    This view processes POST requests containing Papertype information response in JSON format.
    It return  the following fields in the response body:

    - id : The primary key id 
    - papertype: The name of the paper.
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_papertype_response = PaperType.objects.values('id', 'papertype')
            if not exam_papertype_response:
                raise ObjectDoesNotExist("No Data Found")
            
            data = list(exam_papertype_response)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        

class PaperTypeUpdateView(APIView):
    """
    API View to handle the updating of Papertype's records.

    This view processes POST requests to update existing Papertype records.
    It expects the following fields in the request body:

    - id: The id or primary key
    - papertype: The name of the slot.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing Papertype's record.
        
        :param id: Primary key of the Papertype record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_papertype = PaperType.objects.get(id=id)
            serliazer = PaperTypeSerializer(exam_papertype,data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except PaperType.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class PaperTypeDeleteView(APIView):
    """
    API View to handle the deletion of ExamDetails records.

    This view processes DELETE requests to remove existing paper type records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing Papertype record.
        
        param id: Primary key of the Paper type record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_papertype = PaperType.objects.get(id=id)
            exam_papertype.delete()
            return Response({"api_status": True, "message": "Data Deleted Successfully"})

        except PaperType.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})
        
# Exam Mode API's
class ExamModeView(APIView):
    """
    API View to handle the creation of Exam Mode  records.

    This view processes POST requests containing ExamMode information in JSON format.
    It expects the following fields in the request body:

    - exam_mode: The name of exam mode.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serliazer = ExamModeSerializer(data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        
class ExamModeListView(APIView):
    """
    API View to handle the list of Exam Mode records.

    This view processes POST requests containing Exam Mode information response in JSON format.
    It return  the following fields in the response body:

    - id : The primary key id 
    - exam_mode: The name of the exam mode.
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_mode_response = ExamMode.objects.values('id', 'exammode')
            if not exam_mode_response:
                raise ObjectDoesNotExist("No Data Found")
            
            data = list(exam_mode_response)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        

class ExamModeUpdateView(APIView):
    """
    API View to handle the updating of Exam Mode's records.

    This view processes POST requests to update existing Papertype records.
    It expects the following fields in the request body:

    - id: The id or primary key
    - papertype: The name of the slot.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing Exam Mode record.
        
        :param id: Primary key of the Exam Mode record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_mode = ExamMode.objects.get(id=id)
            serliazer = ExamModeSerializer(exam_mode,data=data)

            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except ExamMode.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamModeDeleteView(APIView):
    """
    API View to handle the deletion of Exam Mode records.

    This view processes DELETE requests to remove existing exam mode records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing exam mode record.
        
        param id: Primary key of the exam mode record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            exam_mode = ExamMode.objects.get(id=id)
            exam_mode.delete()
            return Response({"api_status": True, "message": "Data Deleted Successfully"})
        except ExamMode.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})

## Dropdown API'S
# Distinct Exam Code API 
class ExamCodeListView(APIView):

    def get(self,request,*args,**kwargs):

        try:
            # Query to Serve Data
            distinct_exam_codes = ExamDetails.objects.all().values_list('examcode',flat=True).distinct()
            return Response({"api_status":True,"data":distinct_exam_codes})
        except Exception as e:
            return Response({"api_status":False,"message":str(e)})

# Exam Mode Dropdown API's
class ExamModeDropdownView(APIView):

    def post(self,request,*args,**kwargs):

        try:
            # Query to Serve Data
            distinct_exam_mode = ExamMode.objects.all().values_list('exammode',flat=True).distinct()
            return Response({"api_status":True,"data":distinct_exam_mode})
        except Exception as e:
            return Response({"api_status":False,"message":str(e)})


# Region Dropdown API's
class RegionDropdownView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            
            data = JSONParser().parse(request)
            exam_code = data.get('examcode')
            
            # Fetching examcode pf
            exam_details = ExamDetails.objects.get(examcode=exam_code)
            exam_id = exam_details.pk
            
           # Query to Serve Data
            region_names = Region.objects.filter(examcode=exam_id).values_list('regionname', flat=True).distinct()
            
            return Response({"api_status": True, "data": region_names})
        
        except ExamDetails.DoesNotExist:
            return Response({"api_status": False, "message": f"No exam details found for the provided examcode: {exam_code}"})
        
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# State Dropdown API's
class StateDropdownView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            exam_code = data.get('examcode')
            region_name = data.get('regionname')

            # Fetching excamcode pk
            exam_details = ExamDetails.objects.get(examcode=exam_code)
            exam_id = exam_details.pk

            # Fetching region pk
            region = Region.objects.get(regionname=region_name)
            region_id = region.pk

            # Query to Serve Data
            state_names = State.objects.filter(examcode=exam_id, examregion=region_id).values_list('statename', flat=True).distinct()

            return Response({"api_status": True, "data": state_names})

        except ExamDetails.DoesNotExist:
            return Response({"api_status": False, "message": f"No exam details found for the provided examcode: {exam_code}"})

        except Region.DoesNotExist:
            return Response({"api_status": False, "message": f"No region found for the region name: {region_name}"})

        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# City Dropdown API's
class CityDropdownView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            exam_code = data.get('examcode')
            region_name = data.get('regionname')
            state_name = data.get('examstate')

            # Fetching excamcode pk
            exam_details = ExamDetails.objects.get(examcode=exam_code)
            exam_id = exam_details.pk

            # Fetching region pk
            region = Region.objects.get(regionname=region_name)
            region_id = region.pk

            # Fetching state pk
            state = State.objects.get(statename = state_name)
            state_id = state.pk

            # Query to Serve Data
            city_names = City.objects.filter(examcode=exam_id, examregion=region_id ,examstate=state_id).values_list('cityname', flat=True).distinct()

            return Response({"api_status": True, "data": city_names})

        except ExamDetails.DoesNotExist:
            return Response({"api_status": False, "message": f"No exam details found for the provided examcode: {exam_code}"})

        except Region.DoesNotExist:
            return Response({"api_status": False, "message": f"No region found for the region name: {region_name}"})
        
        except State.DoesNotExist:
            return Response({"api_status": False, "message": f"No state found for the state name: {state_name}"})
        
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})

# Rating Dropdown List
class RatingDropdownView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            rating_choices = ExamCenter._meta.get_field('center_rating').choices
            rating_dropdown_list = [value for key, value in rating_choices]
            
            if len(rating_dropdown_list) == 0:
                raise ObjectDoesNotExist("Rating record does not found")
            else:
                return Response({"api_status": True, "data": rating_dropdown_list})

        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# Status Dropdown List
class CenterStatusDropdownView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            ccstatus_choices = ExamCenter._meta.get_field('center_status').choices
            centerstatus_dropdown_list = [value for key, value in ccstatus_choices]
            
            if len (centerstatus_dropdown_list) == 0:
                raise ObjectDoesNotExist("Rating record does not found")
            else:
                return Response({"api_status": True, "data": centerstatus_dropdown_list})

        except Exception as e:
            return Response({"api_status": False, "message": str(e)}) 


# Exam Member Role Dropdown API's
class ExamMemberRoleDropdownView(APIView):

    def post(self,request,*args,**kwargs):

        try:
            # Query to Serve Data
            distinct_exam_role = ExamRole.objects.all().values_list('roletype',flat=True).distinct()
            return Response({"api_status":True,"data":distinct_exam_role})
        except Exception as e:
            return Response({"api_status":False,"message":str(e)})
        


# Status Dropdown List
class MemberTypeDropdownView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            membertype_choices = ExamMember._meta.get_field('membertype').choices
            member_type_dropdown_list = [value for key, value in membertype_choices]
            
            if len (member_type_dropdown_list) == 0:
                raise ObjectDoesNotExist("Rating record does not found")
            else:
                return Response({"api_status": True, "data": member_type_dropdown_list})

        except Exception as e:
            return Response({"api_status": False, "message": str(e)}) 

# Exam Region's API's 
class RegionView(APIView):
    """
    API View to handle the creation of Exam Regions  records.

    This view processes POST requests containing Regions information in JSON format.
    It expects the following fields in the request body:

    - region name: The name of exam mode.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)

            region_name = data['regionname']
            exam_code = data['examcode']
            

            # Fetching examcode pk
            try:
                examcode_examdetails = ExamDetails.objects.get(examcode = exam_code)
            except ExamDetails.DoesNotExist:
                raise ObjectDoesNotExist(f"Exam Code {exam_code} Not found")
            
            data['examcode']= examcode_examdetails.pk
            
            # Checking Existance
            check_existance = Region.objects.filter(regionname = region_name,examcode_id = examcode_examdetails.pk)

            if check_existance.exists():
                return Response({"api_status":False,"message":f"Region - {region_name} and ExamCode - {exam_code} Already Exist"})
            
            serliazer = RegionSerializer(data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        
class RegionListView(APIView):
    """
    API View to handle the list of Regions records.

    This view processes POST requests containing Regions information response in JSON format.
    It return  the following fields in the response body:

    - id : The primary key id 
    - exam_mode: The name of the Regions.
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_region_response = Region.objects.select_related('examcode').values('id','regionname','examcode__examcode')

            if not exam_region_response.exists():
                raise ObjectDoesNotExist("No Data Found") 
                       
            data = list(exam_region_response)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            # print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        

class RegionUpdateView(APIView):
    """
    API View to handle the updating of Regions records.

    This view processes POST requests to update existing Regions records.
    It expects the following fields in the request body:

    - id: The id or primary key
    - papertype: The name of the Regions.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing Exam Mode record.
        
        :param id: Primary key of the Exam Mode record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            
            try:
                exam_mode = Region.objects.get(id=id)
            except Region.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")
            
            # exam code update
            current_examcode_id = exam_mode.examcode.id if exam_mode.examcode else None
            examcode_name = data.get('examcode__examcode')
            if examcode_name:
                try:
                    examcode_instance = ExamDetails.objects.get(examcode=examcode_name)
                    if examcode_instance.id != current_examcode_id:
                        data['examcode'] = examcode_instance.id
                except ExamDetails.DoesNotExist:
                    return Response({"api_status": False, "message": f"Exam code '{examcode_name}' does not exist."})

            # validate data    
            serliazer = RegionSerializer(exam_mode,data=data)

            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except ExamMode.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class RegionDeleteView(APIView):
    """
    API View to handle the deletion of Regions records.

    This view processes DELETE requests to remove existing Regions records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing Regions record.
        
        param id: Primary key of the Regions record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            
            try:
                exam_mode = Region.objects.get(id=id)
            except Region.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")
                
            region_name = exam_mode.regionname
            exam_mode.delete()
            return Response({"api_status": True, "message": f"Region Name {region_name} Deleted Successfully"})
        except Region.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# State API's View
class StateView(APIView):
    """
    API View to handle the creation of Exam Regions  records.

    This view processes POST requests containing Regions information in JSON format.
    It expects the following fields in the request body:

    - region name: The name of exam mode.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)

            region_name = data['examregion']
            exam_code = data['examcode']
            state_name = data['statename']

            # Fetching examcode pk
            examcode_examdetails = ExamDetails.objects.get(examcode = exam_code)
            if not examcode_examdetails:
                raise ObjectDoesNotExist(f"{exam_code} Not found")
            data['examcode']= examcode_examdetails.pk


            # Fetching examregion pk
            regionid_region = Region.objects.get(regionname = region_name , examcode = examcode_examdetails.pk)
            if not regionid_region:
                raise ObjectDoesNotExist(f"{region_name} Not found")
            data['examregion'] = regionid_region.pk
            
            # Checking Existance
            check_existance = State.objects.filter(examregion = regionid_region.pk,examcode_id = examcode_examdetails.pk ,statename = state_name)

            if check_existance:
                return Response({"api_status":False,"message":f"Region - {region_name} and State - {state_name} and ExamCode - {exam_code} Already Exist"})
            
            serliazer = StateSerializer(data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        
class StateListView(APIView):
    """
    API View to handle the list of State records.

    This view processes POST requests containing State information response in JSON format.
    It return  the following fields in the response body:

    - id : The primary key id 
    - exam_mode: The name of the State.
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_state_response = State.objects.select_related('examregion','examcode').values('id','statename',
                                                                                               'examregion__regionname',
                                                                                               'examcode__examcode')
            
            if not exam_state_response:
                raise ObjectDoesNotExist("No Data Found")  
                      
            data = list(exam_state_response)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        

class StateUpdateView(APIView):
    """
    API View to handle the updating of State records.

    This view processes POST requests to update existing Papertype records.
    It expects the following fields in the request body:

    - id: The id or primary key
    - papertype: The name of the slot.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing State record.
        
        :param id: Primary key of the State record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            try:
                exam_mode = State.objects.get(id=id)
            except State.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")

            # exam code update
            current_examcode_id = exam_mode.examcode.id if exam_mode.examcode else None
            
            examcode_name = data.get('examcode__examcode')
            if examcode_name:
                try:
                    examcode_instance = ExamDetails.objects.get(examcode=examcode_name)
                    if examcode_instance.id != current_examcode_id:
                        data['examcode'] = examcode_instance.id
                except ExamDetails.DoesNotExist:
                    return Response({"api_status": False, "message": f"Exam code '{examcode_name}' does not exist."})
            
            # exam region update
            current_statecode_id = exam_mode.examregion.id if exam_mode.examregion else None
            
            examregion_name = data.get('examregion__regionname')
            if examregion_name:
                try:
                    examregion_instance = Region.objects.get(regionname=examregion_name)
                    if examregion_instance.id != current_statecode_id:
                        data['examregion'] = examregion_instance.id
                except Region.DoesNotExist:
                    return Response({"api_status": False, "message": f"Region Name '{examregion_name}' does not exist."})

            # validate data 
            serliazer = StateSerializer(exam_mode,data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except ExamMode.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class StateDeleteView(APIView):
    """
    API View to handle the deletion of State records.

    This view processes DELETE requests to remove existing State records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing State record.
        
        param id: Primary key of the State record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            
            try:
                exam_mode = State.objects.get(id=id)
            except State.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")
            
            state_name = exam_mode.statename
            exam_mode.delete()
            return Response({"api_status": True, "message": f"State Name {state_name} Deleted Successfully"})
        except State.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})
        

# City API's
class CityView(APIView):
    """
    API View to handle the creation of Exam Regions  records.

    This view processes POST requests containing Regions information in JSON format.
    It expects the following fields in the request body:


    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)

            region_name = data['examregion']
            exam_code = data['examcode']
            state_name = data['statename']
            city_name = data['cityname']

            # Fetching examcode pk
            examcode_examdetails = ExamDetails.objects.get(examcode = exam_code)
            if not examcode_examdetails:
                raise ObjectDoesNotExist(f"{exam_code} Not found")
            data['examcode']= examcode_examdetails.pk


            # Fetching examregion pk
            regionid_region = Region.objects.get(regionname = region_name , examcode = examcode_examdetails.pk)
            if not regionid_region:
                raise ObjectDoesNotExist(f"{region_name} Not found")
            data['examregion'] = regionid_region.pk


            # Fetching state pk
            stateid_state = State.objects.get(examregion = regionid_region.pk, examcode = examcode_examdetails.pk,statename =state_name)
            if not stateid_state:
                raise ObjectDoesNotExist(f"{state_name} Not found")   
            data['examstate'] = stateid_state.pk

            # Checking Existance
            check_existance = City.objects.filter(examregion = regionid_region.pk,examcode_id = examcode_examdetails.pk ,examstate = stateid_state.pk ,cityname = city_name )

            if check_existance:
                return Response({"api_status":False,"message":f"Region - {region_name} and State - {state_name} and  City - {state_name} and ExamCode - {exam_code} Already Exist"})
            
            serliazer = CitySerializer(data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        
class CityListView(APIView):
    """
    API View to handle the list of State records.

    This view processes POST requests containing State information response in JSON format.
    It return  the following fields in the response body:

    - id : The primary key id 
    - exam_mode: The name of the State.
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_state_response = City.objects.select_related('examstate', 'examregion', 'examcode').values('id','cityname','examstate__statename',
                                                                                                            'examregion__regionname',
                                                                                                            'examcode__examcode')


            if not exam_state_response:
                raise ObjectDoesNotExist("No Data Found") 
                       
            data = list(exam_state_response)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})
        

class CityUpdateView(APIView):
    """
    API View to handle the updating of State records.

    This view processes POST requests to update existing Papertype records.
    It expects the following fields in the request body:

    - id: The id or primary key
    - papertype: The name of the slot.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing State record.
        
        :param id: Primary key of the State record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')

            try:
                exam_mode = City.objects.get(id=id)
            except City.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")

            if not exam_mode :
                return Response({"api_status":False,"message":"Record Not Found"})

            # exam code update
            current_examcode_id = exam_mode.examcode.id if exam_mode.examcode else None
            
            examcode_name = data.get('examcode__examcode')
            if examcode_name:
                try:
                    examcode_instance = ExamDetails.objects.get(examcode=examcode_name)
                    if examcode_instance.id != current_examcode_id:
                        data['examcode'] = examcode_instance.id
                except ExamDetails.DoesNotExist:
                    return Response({"api_status": False, "message": f"Exam code '{examcode_name}' does not exist."})
            
            # exam region update
            current_region_id = exam_mode.examregion.id if exam_mode.examregion else None
            
            examregion_name = data.get('examregion__regionname')
            if examregion_name:
                try:
                    examregion_instance = Region.objects.get(regionname=examregion_name)
                    if examregion_instance.id != current_region_id:
                        data['examregion'] = examregion_instance.id
                except Region.DoesNotExist:
                    return Response({"api_status": False, "message": f"Region Name '{examregion_name}' does not exist."})
            
            # exam state update
            current_statecode_id = exam_mode.examstate.id if exam_mode.examstate else None
            
            examstate_name = data.get('examstate__statename')
            if examstate_name:
                try:
                    examstate_instance = State.objects.get(statename=examstate_name)
                    if examstate_instance.id != current_statecode_id:
                        data['examstate'] = examstate_instance.id
                except Region.DoesNotExist:
                    return Response({"api_status": False, "message": f"Region Name '{examstate_name}' does not exist."})
            
            # validate data            
            serliazer = CitySerializer(exam_mode,data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except ExamMode.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class CityDeleteView(APIView):
    """
    API View to handle the deletion of State records.

    This view processes DELETE requests to remove existing State records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing State record.
        
        param id: Primary key of the State record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            
            try:
                exam_mode = City.objects.get(id=id)
            except City.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")
            
            city_name = exam_mode.cityname
            exam_mode.delete()
            return Response({"api_status": True, "message": f"City Name {city_name} Deleted Successfully"})
        except State.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})        
        

# Center API's
class CenterView(APIView):
    """
    API View to handle the creation of Exam Centers records.

    This view processes POST requests containing Centers information in JSON format.
    It expects the following fields in the request body:

    - will provide
    """

    def post(self, request, *args , **kwargs):
        try:
            print("calling center api")
            data = JSONParser().parse(request)
            
            center_code = data['centercode']
            exam_code = data['examcode']
            exam_mode = data['exammode']
            exam_region = data['examregion']
            exam_state = data['examstate']
            exam_city = data['examcity']

            # Fetching examcode pk    
            examcode_pk = get_pk(ExamDetails,{"examcode":exam_code})
            if not examcode_pk:
                raise ObjectDoesNotExist(f"{exam_code} Not Found")
            else:
                data['examcode'] = examcode_pk

            # Fetching exam_mode pk
            examcode_filter_fields = {"exammode":exam_mode}   
            exammode_pk = get_pk(ExamMode,examcode_filter_fields)
            if not exammode_pk:
                raise ObjectDoesNotExist(f"{exam_mode} Not Found")
            else:
                data['exammode'] = exammode_pk
                
            # Fetching exam_region pk
            examregion_filter_fields = {"regionname":exam_region,"examcode":examcode_pk}     
            examregion_pk = get_pk(Region,examregion_filter_fields)
            if not examregion_pk:
                raise ObjectDoesNotExist(f"{exam_region} Not Found")
            else:
                data['examregion'] = examregion_pk

            # Fetching exam_state pk
            exam_state_filters = {"statename":exam_state,"examregion":examregion_pk,"examcode":examcode_pk}
            examstate_pk = get_pk(State,exam_state_filters)
            if not examstate_pk:
                raise ObjectDoesNotExist(f"{exam_state} Not Found")
            else:
                data['examstate'] = examstate_pk

            # Fetching exam_city pk
            exam_city_filters = {"cityname":exam_city,"examstate":examstate_pk,"examregion":examregion_pk,"examcode":examcode_pk}
            examcity_pk = get_pk(City,exam_city_filters)
            if not examcity_pk:
                raise ObjectDoesNotExist(f"{exam_city} Not Found")
            else:
                data['examcity'] = examcity_pk

            check_center_existance = ExamCenter.objects.filter(centercode = center_code , examcode = examcode_pk)

            if check_center_existance.exists():
                return Response({"api_status":False,"message":f"centercode - {center_code} & examcode - {exam_code} Already Exist"})
            else:    
                serliazer = ExamCenterSerializer(data=data)
                if serliazer.is_valid():
                    serliazer.save()
                    return Response({"api_status": True, "message": "Data Saved Successfully"})
                else:
                    return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
        except Exception as e:
            return Response({"api_staus":False,"message":str(e)})
        

class CenterListView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            center_view_list = ExamCenter.objects.values('id',  # Primary key
                                                        'centercode', 'centername', 'center_address', 'center_landmark', 'contact_person_name', 'center_email',
                                                        'center_contact', 'center_pincode', 'center_google_mapurl', 'center_latitude', 'center_longitude',
                                                        'center_status', 'center_rating', 'center_capacity', 'record_created_at', 'record_updated_at',
                                                        'record_created_by', 'record_updated_by', 'isactive', 'remarks','center_contact_alternate',
                                                        'examcode__examcode', 'exammode__exammode', 'examregion__regionname', 'examstate__statename', 'examcity__cityname')
            
            if not center_view_list.exists():
                # raise ObjectDoesNotExist("No Data Found")
                return Response({"api_status":True,"data":object_not_exist})


            data = list(center_view_list)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            return Response({"api_status":False,"message":str(e)})


class CenterUpdateView(APIView):
    """
    API View to handle the updating of State records.

    This view processes POST requests to update existing Papertype records.
    It expects the following fields in the request body:

    - id: The id or primary key
    - papertype: The name of the slot.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing State record.
        
        :param id: Primary key of the State record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')

            try:
                exam_mode = ExamCenter.objects.get(id=id)
            except ExamCenter.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")

            if not exam_mode :
                return Response({"api_status":False,"message":"Record Not Found"})

            # exam code update
            current_examcode_id = exam_mode.examcode.id if exam_mode.examcode else None
            
            examcode_name = data.get('examcode__examcode')
            if examcode_name:
                try:
                    examcode_instance = ExamDetails.objects.get(examcode=examcode_name)
                    if examcode_instance.id != current_examcode_id:
                        data['examcode'] = examcode_instance.id
                except ExamDetails.DoesNotExist:
                    return Response({"api_status": False, "message": f"Exam code '{examcode_name}' does not exist."})

            # exam mode update
            current_exammode_id = exam_mode.exammode.id if exam_mode.exammode else None
            
            exammode_name = data.get('examcode__exammode')
            if exammode_name:
                try:
                    exammode_instance = ExamMode.objects.get(exammode=exammode_name)
                    if exammode_instance.id != current_exammode_id:
                        data['exammode'] = exammode_instance.id
                except ExamMode.DoesNotExist:
                    return Response({"api_status": False, "message": f"Exam mode '{exammode_name}' does not exist."})    
            
            # exam region update
            current_region_id = exam_mode.examregion.id if exam_mode.examregion else None
            
            examregion_name = data.get('examregion__regionname')
            if examregion_name:
                try:
                    examregion_instance = Region.objects.get(regionname=examregion_name)
                    if examregion_instance.id != current_region_id:
                        data['examregion'] = examregion_instance.id
                except Region.DoesNotExist:
                    return Response({"api_status": False, "message": f"Region Name '{examregion_name}' does not exist."})
            
            # exam state update
            current_statecode_id = exam_mode.examstate.id if exam_mode.examstate else None
            
            examstate_name = data.get('examstate__statename')
            if examstate_name:
                try:
                    examstate_instance = State.objects.get(statename=examstate_name)
                    if examstate_instance.id != current_statecode_id:
                        data['examstate'] = examstate_instance.id
                except Region.DoesNotExist:
                    return Response({"api_status": False, "message": f"State Name '{examstate_name}' does not exist."})
                
            # exam city update
            current_city_id = exam_mode.examcity.id if exam_mode.examcity else None
            
            examcity_name = data.get('examcity__cityname')
            if examcity_name:
                try:
                    examcity_instance = City.objects.get(cityname=examcity_name)
                    if examcity_instance.id != current_city_id:
                        data['examcity'] = examcity_instance.id
                except City.DoesNotExist:
                    return Response({"api_status": False, "message": f"City Name '{examcity_name}' does not exist."})
            
            # validate data            
            serliazer = ExamCenterSerializer(exam_mode,data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})

        except ExamMode.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# update-check
class CenterUpdate(APIView):
        
        def post(self, request, *args, **kwargs):
            """
            Handles POST requests to update an existing State record.
            
            :param id: Primary key of the State record to be updated.
            """
            try:
                data = JSONParser().parse(request)
                id = data.get('id')

                try:
                    exam_mode = ExamCenter.objects.get(id=id)
                except ExamCenter.DoesNotExist:
                    raise ObjectDoesNotExist("Record Not Found")

                if not exam_mode.exist() :
                    return Response({"api_status":False,"message":"Record Not Found"})
                
                update_mode = ExamCenter.objects.filter(id=id).update(**data)
                update_mode.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            except Exception as e:
                return Response({"api_status": False, "message": str(e)})
# update-check

class CenterDeleteView(APIView):
    """
    API View to handle the deletion of Center records.

    This view processes POST requests to remove existing Regions records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing center record.
        
        param id: Primary key of the center record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            
            try:
                exam_mode = ExamCenter.objects.get(id=id)
            except ExamCenter.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")
                
            center_name = exam_mode.centercode
            exam_mode.delete()
            return Response({"api_status": True, "message": f"Centercode  {center_name} Deleted Successfully"})
        except Region.DoesNotExist:
            return Response({"api_status": False, "message": "Record not found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# Exam Device API's
class ExamDeviceView(APIView):
    """
    API View to handle the creation of ExamDevice records.
    
    This view processes POST requests containing device information in JSON format.
    It expects the following fields in the request body:
    
    - device_no: The unique device number.
    - device_name: The name of the device.
    - macid: The MAC ID of the device.
    - modelname: The model name of the device.
    - manufacturer: The manufacturer of the device.
    - dateof_boarding: The boarding date of the device (optional).
    - image_version: The image version of the device (optional).
    - is_mapped: Indicates whether the device is mapped (default is 0).
    - rough_score: The rough score associated with the device (optional).
    - dev_fingerprint: The fingerprint of the device (optional).
    - no_of_interface: The number of interfaces available (optional).
    - record_created_by: The user who created the record.
    - record_updated_by: The user who updated the record.
    - isactive: Indicates if the device is active (default is True).
    - remarks: Additional remarks about the device (optional).
    """
    
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            check_existence = ExamDevice.objects.filter(device_no=data['device_no'])
            if check_existence:
                return Response({"api_status": False, "message": f"Device number {data['device_no']} already exists"})
            else:
                serializer = ExamDeviceSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"api_status": True, "message": "Data Saved Successfully"})
                else:
                    return Response({"api_status": False, "message": "Invalid Input Format", "Error": serializer.errors})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamDeviceUpdateView(APIView):
    """
    API View to handle the updating of ExamDevice records.
    
    This view processes POST requests containing the updated device information in JSON format.
    It expects the device_no to identify the device to be updated and other fields to update.
    """
    
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            device_no = data.get('device_no')
            try:
                device = ExamDevice.objects.get(device_no=device_no)
                serializer = ExamDeviceSerializer(device, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"api_status": True, "message": "Data Updated Successfully"})
                else:
                    return Response({"api_status": False, "message": "Invalid Input Format", "Error": serializer.errors})
            except ExamDevice.DoesNotExist:
                return Response({"api_status": False, "message": f"Device number {device_no} does not exist"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamDeviceListView(APIView):
    """
    API View to handle the listing of ExamDevice records.
    """
    def post(self, request, *args, **kwargs):
        try:
            devices = ExamDevice.objects.all()
            serializer = ExamDeviceSerializer(devices, many=True)
            return Response({"api_status": True, "data": serializer.data})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})
        

class ExamDeviceDeleteView(APIView):
    """
    API View to handle the deletion of ExamDevice records.
    
    This view processes POST requests containing the device_no to identify the device to be deleted.
    """
    
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            device_no = data.get('device_no')
            try:
                device = ExamDevice.objects.get(device_no=device_no)
                device.delete()
                return Response({"api_status": True, "message": "Device Deleted Successfully"})
            except ExamDevice.DoesNotExist:
                return Response({"api_status": False, "message": f"Device number {device_no} does not exist"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# Exam Role API's
class ExamRoleView(APIView):
    """
    API to create a new ExamRole record.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)

            # Check if a role with the same roletype already exists
            if ExamRole.objects.filter(roletype=data.get('roletype')).exists():
                return Response({"api_status": False, "message": f"Role '{data['roletype']}' already exists."})

            serializer = ExamRoleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            return Response({"api_status": False, "message": "Invalid Input", "Error": serializer.errors})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})



class ExamRoleListView(APIView):
    """
    API to list all ExamRole records.
    """
    def post(self, request, *args, **kwargs):
        try:
            roles = ExamRole.objects.all()
            serializer = ExamRoleSerializer(roles, many=True)
            return Response({"api_status": True, "data": serializer.data})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamRoleUpdateView(APIView):
    """
    API to update an existing ExamRole record.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            try:
                role = ExamRole.objects.get(id=id)
            except ExamRole.DoesNotExist:
                return Response({"api_status": False, "message": "Record Not Found"})

            serializer = ExamRoleSerializer(role, data=data)
            print("data:-",data)
            if serializer.is_valid():
                serializer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input", "Error": serializer.errors})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamRoleDeleteView(APIView):
    """
    API to delete an existing ExamRole record.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            try:
                role = ExamRole.objects.get(id=id)
                role.delete()
                return Response({"api_status": True, "message": "Record Deleted Successfully"})
            except ExamRole.DoesNotExist:
                return Response({"api_status": False, "message": "Record Not Found"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# Exam Member API'S
class ExamMemberView(APIView):
    """
    API to create a new ExamMember record.
    """
    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)

            member_name = data['membername']
            member_role = data['memberrole']

            # Fetching member_role pk
            try:
                member_role = ExamRole.objects.get(roletype = member_role)
                print("member_role",member_role)
            except ExamRole.DoesNotExist:
                raise ObjectDoesNotExist(f"Exam Code {member_role} Not found")
            
            data['memberrole']= member_role.pk
            
            # Checking Existance
            check_existance = ExamMember.objects.filter(membername = member_name,memberrole = member_role.pk)

            if check_existance.exists():
                return Response({"api_status":False,"message":f"Member - {member_name}  Already Exist"})
            
            serliazer = ExamMemberserializer(data=data)
            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Saved Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
        except Exception as e:
            print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})


class ExamMemberListView(APIView):
    """
    API to retrieve the list of ExamMember records.
    """
    def get(self, request, *args, **kwargs):
        try:
            exam_member_response = ExamMember.objects.values('id','membername','memberrole__roletype',
                                                                'email_id','contact_number','alternate_number',
                                                                'membertype')

            if not exam_member_response.exists():
                raise ObjectDoesNotExist("No Data Found") 
                       
            data = list(exam_member_response)
            return Response({"api_status":True,"data":data})
        except Exception as e:
            # print("Exception in e", str(e))
            return Response({"api_status": False, "message": str(e)})


class ExamMemberUpdateView(APIView):
    """
    API View to handle the updating of ExamMember records.

    This view processes POST requests to update existing ExamMember records.
    It expects the following fields in the request body:

    - id: The id or primary key
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update an existing ExamMember record.
        
        :param id: Primary key of the ExamMember record to be updated.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            
            try:
                exam_mode = ExamMember.objects.get(id=id)
            except ExamMember.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")
            
            # exam memberrole update
            current_memberrole_id = exam_mode.memberrole.id if exam_mode.memberrole else None
            memberrole_name = data.get('memberrole__roletype')
            if memberrole_name:
                try:
                    memberrole_instance = ExamRole.objects.get(roletype=memberrole_name)
                    if memberrole_instance.id != current_memberrole_id:
                        data['memberrole'] = memberrole_instance.id
                    else:
                        data['memberrole'] = current_memberrole_id
                except ExamRole.DoesNotExist:
                    return Response({"api_status": False, "message": f"Member role '{memberrole_name}' does not exist."})

            # validate data    
            serliazer = ExamMemberserializer(exam_mode,data=data)

            if serliazer.is_valid():
                serliazer.save()
                return Response({"api_status": True, "message": "Data Updated Successfully"})
            else:
                return Response({"api_status": False, "message": "Invalid Input Format" , "Error":serliazer.errors})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


class ExamMemberDeleteView(APIView):
    """
    API View to handle the deletion of ExamMember records.

    This view processes DELETE requests to remove existing ExamMember records.
    It requires the primary key of the record to be deleted.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to remove an existing Regions record.
        
        param id: Primary key of the Regions record to be deleted.
        """
        try:
            data = JSONParser().parse(request)
            id = data.get('id')
            
            try:
                exam_mode = ExamMember.objects.get(id=id)
            except ExamMember.DoesNotExist:
                raise ObjectDoesNotExist("Record Not Found")
                
            member_name = exam_mode.membername
            exam_mode.delete()
            return Response({"api_status": True, "message": f"Region Name {member_name} Deleted Successfully"})
        except Exception as e:
            return Response({"api_status": False, "message": str(e)})


# Exam Device Mapping 
class ExamDeviceMappingView(APIView):
    def post(self, request, *args, **kwargs):
        pass
