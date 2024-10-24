# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import hashlib
import uuid
from typing import Any
from django.db import models
from django.http import HttpRequest
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch.dispatcher import receiver
from utils.choices import center_status,center_rating,member_type,otp_type,request_priority
import user_agents
		

class ExamDetails(models.Model):
	examname			= models.CharField(max_length=20)
	clientname			= models.CharField(max_length=20)
	examcode	        = models.CharField(max_length=20,unique=True)
	no_of_examdays		= models.PositiveIntegerField()
	no_of_examslot		= models.PositiveIntegerField()
	no_of_regions		= models.PositiveIntegerField()
	no_of_centers		= models.PositiveIntegerField()
	exam_start_date		= models.DateField()
	exam_end_date		= models.DateField()
	mock_start_date		= models.DateField()
	mock_end_date		= models.DateField()
	exam_hash 			= models.CharField(max_length=32, blank=True)
	record_created_at 	= models.DateTimeField(auto_now_add=True)
	record_updated_at   = models.DateTimeField(auto_now=True)
	record_created_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ed_userc")
	record_updated_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ed_useru")
	isactive            = models.BooleanField(default=True)
	remarks 			= models.TextField(max_length=250, blank=True)
	
	def __str__(self):
		return f"{self.examname}-{self.examcode}"
           

class ExamMode(models.Model):
	exammode			= models.CharField(max_length=25,unique=True)
	# examcode 			= models.ForeignKey(ExamDetails,blank=True,null=True,on_delete=models.CASCADE,)
	record_created_at 	= models.DateTimeField(auto_now_add=True)
	record_updated_at   = models.DateTimeField(auto_now=True)
	record_created_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="em_userc")
	record_updated_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="em_useru")
	isactive            = models.BooleanField(default=True)
	remarks 			= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return self.exammode
	
class ExamSlot(models.Model):
	examslot				= models.CharField(max_length=10)
	examcode 				= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,blank=True,null=True)
	download_time			= models.DateTimeField()
	allowdownloadqp			= models.BooleanField(default=False)
	allowdownloadkey		= models.BooleanField(default=False)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="es_userc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="es_useru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return self.slotname

class PaperType(models.Model):
	papertype				= models.CharField(max_length=10)
	examcode 				= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,blank=True,null=True)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="pt_userc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="pt_useru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f"{self.papertype}"

class Region(models.Model):
	regionname			= models.CharField(max_length=25)
	examcode 			= models.ForeignKey(ExamDetails,blank=True,null=True,on_delete=models.CASCADE,)
	record_created_at 	= models.DateTimeField(auto_now_add=True)
	record_updated_at   = models.DateTimeField(auto_now=True)
	record_created_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ruserc")
	record_updated_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ruseru")
	isactive            = models.BooleanField(default=True)
	remarks 			= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return self.regionname
	

class State(models.Model):
	statename			= models.CharField(max_length=30,)
	examregion			= models.ForeignKey(Region,on_delete=models.CASCADE,blank=True,null=True)
	examcode 			= models.ForeignKey(ExamDetails,blank=True,null=True,on_delete=models.CASCADE,)
	created_at 	        = models.DateTimeField(auto_now_add=True)
	updated_at          = models.DateTimeField(auto_now=True)
	created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="suserc")
	updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="suseru")
	isactive            = models.BooleanField(default=True)
	remarks 			= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return self.statename


class City(models.Model):
	cityname			= models.CharField(max_length=30,)
	examregion			= models.ForeignKey(Region,on_delete=models.CASCADE,blank=True,null=True)
	examstate			= models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True)
	examcode 			= models.ForeignKey(ExamDetails,blank=True,null=True,on_delete=models.CASCADE,)
	record_created_at 	= models.DateTimeField(auto_now_add=True)
	record_updated_at   = models.DateTimeField(auto_now=True)
	record_created_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="cuserc")
	record_updated_by	= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="cuseru")
	isactive            = models.BooleanField(default=True)
	remarks 			= models.TextField(max_length=250, blank=True)
	
	def __str__(self):
		return self.cityname

class ExamCenter(models.Model):
	centercode					= models.PositiveIntegerField()
	centername					= models.TextField()
	examcode 					= models.ForeignKey(ExamDetails,blank=True,null=True,on_delete=models.CASCADE,)
	exammode					= models.ForeignKey(ExamMode,on_delete=models.CASCADE,blank=True,null=True)
	examregion					= models.ForeignKey(Region,on_delete=models.CASCADE,blank=True,null=True)
	examstate					= models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True)
	examcity					= models.ForeignKey(City,on_delete=models.CASCADE,blank=True,null=True)
	center_address				= models.TextField()
	center_landmark				= models.CharField(max_length=250,)
	contact_person_name			= models.CharField(max_length=50,)
	center_email				= models.EmailField()
	center_contact 				= models.CharField(max_length=10,)
	center_pincode				= models.CharField(max_length=6,)
	center_google_mapurl		= models.CharField(max_length=250)
	center_latitude				= models.CharField(max_length=250,)
	center_longitude			= models.CharField(max_length=250,)
	center_status				= models.CharField(max_length=50,choices=center_status,)
	center_rating				= models.CharField(max_length=50,choices=center_rating,)
	center_capacity				= models.PositiveIntegerField()
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ec_userc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ec_useru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)
	

	def __str__(self):
		return f"{self.centercode}-{self.centername}-{self.examcode}-{self.exammode}"

class ExamDevice(models.Model):
	device_no 					= models.CharField(max_length=10,unique=True)
	device_name			 		= models.CharField(max_length=25,unique=True)
	macid						= models.CharField(max_length=50,)
	modelname					= models.CharField(max_length=50,)
	manufacturer				= models.CharField(max_length=50)
	dateof_boarding				= models.DateField(blank=True, null=True)
	image_version				= models.CharField(max_length=50,blank=True)
	is_mapped					= models.BooleanField(default=0)
	rough_score                 = models.IntegerField(blank=True, null=True)
	dev_fingerprint				= models.CharField(max_length=50,blank=True)
	no_of_interface             = models.IntegerField(blank=True, null=True)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="eduserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="eduseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)


class ExamRole(models.Model):
	roletype					= models.CharField(max_length=25,unique=True,)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="eruserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="eruseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return self.roletype

class ExamMember(models.Model):
	membername					= models.CharField(max_length=50,)
	memberrole					= models.ForeignKey(ExamRole,on_delete=models.CASCADE)
	email_id					= models.EmailField()
	contact_number				= models.CharField(max_length=10,unique=True)
	alternate_number			= models.CharField(max_length=10,)
	membertype					= models.CharField(max_length=20,choices=member_type,)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="emuserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="emuseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f"{self.membername}-{self.contact_number}"

class CenterDeviceMapping(models.Model):
	examcode            		= models.ForeignKey(ExamDetails,on_delete=models.CASCADE)
	centercode					= models.ForeignKey(ExamCenter,on_delete=models.CASCADE)
	examdevice 					= models.ForeignKey(ExamDevice,on_delete=models.CASCADE)
	islive						= models.BooleanField(default=0)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="edmuserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="edmuseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)


class CenterSlotMapping(models.Model):
	examcode            		= models.ForeignKey(ExamDetails,on_delete=models.CASCADE)
	centercode					= models.ForeignKey(ExamCenter,on_delete=models.CASCADE)
	examslot 					= models.ForeignKey(ExamSlot,on_delete=models.CASCADE)
	papertype					= models.ForeignKey(PaperType, on_delete=models.CASCADE)
	total_count					= models.PositiveIntegerField(default=0)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="csmuserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="csmuseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f"{self.examcode}:{self.centercode}:{self.examslot}:{self.papertype}:{self.total_count}"
		
class CenterCiMapping(models.Model):
	examcode            		= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	centercode	 				= models.ForeignKey(ExamCenter,on_delete=models.CASCADE,null=True,blank=True)
	membername					= models.ForeignKey(ExamMember,on_delete=models.CASCADE,null=True,blank=True)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ccmuserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ccmuseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f'{self.centercode.centername}-{self.membername.membername}'

class ExamScriptUpload(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	examslot 				= models.ForeignKey(ExamSlot,on_delete=models.CASCADE,null=True,blank=True)
	papertype				= models.ForeignKey(PaperType,on_delete=models.CASCADE)
	exam_filename			= models.CharField(max_length=250, unique=True, blank=True,)
	examfile 				= models.FileField(upload_to='examfile/')
	membername				= models.ForeignKey(User, on_delete=models.CASCADE)
	calc_hash				= models.CharField(max_length=250, unique=True, blank=True,)
	upload_hash				= models.CharField(max_length=250, unique=True, blank=True,)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="esuuserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="esuuseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f'{self.examcode}-{self.examslot}-{self.papertype}-{self.exam_filename}'

class QuestionPaperUpload(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	examslot 				= models.ForeignKey(ExamSlot,on_delete=models.CASCADE,null=True,blank=True)
	papertype				= models.ForeignKey(PaperType,on_delete=models.CASCADE)
	qp_filename				= models.CharField(max_length=250, unique=True, blank=True,)
	questionpaper 			= models.FileField(upload_to='qpaper/')
	membername				= models.ForeignKey(User, on_delete=models.CASCADE)
	calc_hash				= models.CharField(max_length=250, unique=True, blank=True,)
	upload_hash				= models.CharField(max_length=250, unique=True, blank=True,)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="qpuuserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="qpuuseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f'{self.examcode}-{self.examslot}-{self.papertype}-{self.qp_filename}'

class DecryptKeyUpload(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	examslot            	= models.ForeignKey(ExamSlot,on_delete=models.CASCADE)
	papertype			 	= models.ForeignKey(PaperType,on_delete=models.CASCADE)
	qp_filename         	= models.ForeignKey(QuestionPaperUpload, on_delete=models.CASCADE)
	key_filename		 	= models.CharField(max_length=250, unique=True, blank=True,)
	decrypt_key 		 	= models.FileField(upload_to='decrypt_key/')
	membername			 	= models.ForeignKey(User, on_delete=models.CASCADE)
	calc_hash		     	= models.CharField(max_length=250, unique=True, blank=True,)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="dkuuserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="dkuuseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)
      
	def __str__(self):
		return f'{self.examcode}-{self.examslot}-{self.papertype}-{self.key_filename}'
          

class ExamServerOTP(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	user_center     		= models.ForeignKey(User,on_delete=models.CASCADE)
	otp_type 				= models.CharField(max_length=25,choices=otp_type)
	otp 					= models.CharField(max_length=250, unique=True,)
	otp_api_id				= models.CharField(max_length=100,blank=True,null=True)
	contact_number  		= models.CharField(max_length=10,)
	status 					= models.CharField(max_length=10,)
	expiry					= models.DateTimeField()
	used_at					= models.DateTimeField(null=True, blank=True,)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="esouserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="esouseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f'{self.examcode}-{self.user_center}-{self.otp}'


class ExamServerRegistration(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	centercode 				= models.ForeignKey(ExamCenter, blank=True,null=True, on_delete=models.CASCADE)
	examdevice 				= models.ForeignKey(ExamDevice,on_delete=models.CASCADE)
	pxe_ip					= models.CharField(max_length=25)
	primary_ip				= models.CharField(max_length=25,)
	secondary_ip			= models.CharField(max_length=25,)
	ciname					= models.CharField(max_length=50,)
	cicontact				= models.CharField(max_length=10,)
	macid					= models.CharField(max_length=50,)
	hdserial				= models.CharField(max_length=50,blank=True)
	servertype				= models.CharField(max_length=50,blank=True)
	no_of_request 			= models.IntegerField()
	keyidentifier			= models.CharField(max_length=250,blank=True)
	serverkey 				= models.FileField(upload_to='serverkey/',)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="esruserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="esruseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return self.centercode.centername


class ExamCenterRequest(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	centercode 				= models.ForeignKey(ExamCenter, blank=True,null=True, on_delete=models.CASCADE)
	examslot 				= models.ForeignKey(ExamSlot, null=True, blank=True, on_delete=models.CASCADE)
	papertype 				= models.ForeignKey(PaperType, null=True, blank=True, on_delete=models.CASCADE)
	request_type			= models.CharField(max_length=250,)
	request_priority		= models.CharField(max_length=250,choices=request_priority)
	remote_address			= models.CharField(max_length=50)
	server_status 			= models.CharField(max_length=250,)
	client_status 			= models.CharField(max_length=250,)
	requesttime				= models.DateTimeField()
	qpack_hash				= models.CharField(max_length=250, blank=True,)
	download_again			= models.BooleanField(default=False) 
	client_acktime			= models.DateTimeField(null=True)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ecruserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="ecruseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return f"{self.examcode}-{self.centercode.centername}-{self.request_type}-{self.remarks}"



class UserProfile(models.Model):
	examcode            		= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	username 					= models.ForeignKey(User, on_delete=models.CASCADE)
	contact_number				= models.CharField(max_length=10)
	status						= models.BooleanField(default=True)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="upuserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="upuseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)

	def __str__(self):
			return self.username.username
	
class ExamRegionHead(models.Model):
	examcode            		= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	username 					= models.ForeignKey(User, on_delete=models.CASCADE,)
	examregion					= models.ForeignKey(Region, on_delete=models.CASCADE,)
	membername         			= models.ForeignKey(ExamMember, on_delete=models.CASCADE)
	status						= models.BooleanField(default=True)
	record_created_at 			= models.DateTimeField(auto_now_add=True)
	record_updated_at   		= models.DateTimeField(auto_now=True)
	record_created_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="erhuserc")
	record_updated_by			= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="erhuseru")
	isactive            		= models.BooleanField(default=True)
	remarks 					= models.TextField(max_length=250, blank=True)

	def __str__(self):
			return f'{self.examcode}-{self.examregion}-{self.username}'



class EncKeyStore(models.Model):
	toprocess				= models.CharField(max_length=250,)
	symkey 					= models.CharField(max_length=250,)
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	examslot 				= models.ForeignKey(ExamSlot, on_delete=models.CASCADE, blank=True, null=True)
	papertype				= models.ForeignKey(PaperType, on_delete=models.CASCADE, blank=True, null=True)
	status 					= models.BooleanField(default=False)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="eksuserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="eksuseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)
	
	def __str__(self):
			return f"{self.examcode}-{self.examslot.slotname}-{self.toprocess}"


class ResponseSheet(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	centercode	 			= models.ForeignKey(ExamCenter, on_delete=models.CASCADE)
	examslot 				= models.ForeignKey(ExamSlot, on_delete=models.CASCADE)
	papertype				= models.ForeignKey(PaperType, on_delete=models.CASCADE,null=True)
	response_sheet 			= models.FileField(upload_to='response_sheet/',max_length=700)
	hashvalue				= models.CharField(max_length=250, default=None,)
	pxeupload_status 		= models.BooleanField(default=False)
	transfer_status 		= models.BooleanField(default=0)
	transferred_time 		=  models.DateTimeField(null=True, blank=True)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="rsuserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="rsuseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return "{0}-{1}-{2}-{3}-{4}".format(self.examcode,self.centercode.centercode, self.examslot.slotname,self.papertype.papertype,self.response_sheet)
    
class LabDetail(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	centercode	 			= models.ForeignKey(ExamCenter, on_delete=models.CASCADE)
	examslot				= models.ForeignKey(ExamSlot, on_delete=models.CASCADE, blank=True, null=True)
	labname 				= models.CharField(max_length=255)	
	labcapacity				= models.CharField(max_length=255)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="lduserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="lduseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)
    
	def __str__(self):
		return "{0}-{1}-{2}".format(self.examcode,self.centercode.centercode,self.slotname)

class UserSlotMapping(models.Model):
	examcode            	= models.ForeignKey(ExamDetails,on_delete=models.CASCADE,null=True,blank=True)
	username 				= models.ForeignKey(User, on_delete=models.CASCADE)
	mappedslots 			= models.TextField(blank=True)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="usmuserc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="usmuseru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)

	def __str__(self):
		return "{0}-{1}-{2}".format(self.examcode,self.username, self.mappedslots)

class UserSession(models.Model):
	user 					= models.ForeignKey(User, on_delete=models.CASCADE)
	session 				= models.OneToOneField(Session, on_delete=models.CASCADE)
	record_created_at 		= models.DateTimeField(auto_now_add=True)
	record_updated_at   	= models.DateTimeField(auto_now=True)
	record_created_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="uususerc")
	record_updated_by		= models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE,related_name="uususeru")
	isactive            	= models.BooleanField(default=True)
	remarks 				= models.TextField(max_length=250, blank=True)	


class UserVisitManager(models.Manager):
    """Custom model manager for UserVisit objects."""

    def parse_remote_addr(self, request: HttpRequest) -> str:
        """Extract client IP from request."""
        x_forwarded_for = request.headers.get("X-Forwarded-For", "")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "").strip()

    def parse_ua_string(self, request: HttpRequest) -> str:
        """Extract client user-agent from request."""
        return request.headers.get("User-Agent", "").strip()

    def build(self, request: HttpRequest, timestamp: datetime) -> 'UserVisit':
        """Build a new UserVisit object from a request, without saving it."""
        uv = UserVisit(
            user=request.user,
            session_start=timestamp,
            session_key=request.session.session_key,
            remote_addr=self.parse_remote_addr(request),
            ua_string=self.parse_ua_string(request),
        )
        uv.hash = uv.md5().hexdigest()  # Assuming md5() is a method on UserVisit
        return uv


class UserVisit(models.Model):
    user = models.ForeignKey(
        User, related_name="user_visits", on_delete=models.CASCADE
    )
    session_start = models.DateTimeField(
        help_text="The time at which the first visit of the day was recorded",
        default=timezone.now,
    )
    session_key = models.CharField(help_text="Django session identifier", max_length=40)
    remote_addr = models.CharField(
        help_text=(
            "Client IP address (from X-Forwarded-For HTTP header, "
            "or REMOTE_ADDR request property)"
        ),
        max_length=100,
        blank=True,
    )
    last_accessed = models.DateTimeField(help_text="User Last Access Time", default=None, null=True)
    session_end = models.DateTimeField(help_text="User Session Active Upto this time", default=None, null=True)
    ua_string = models.TextField(
        "User agent (raw)",
        help_text="Client User-Agent HTTP header",
        blank=True,
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_agent = models.CharField("Actual User Agent",help_text="User Agent Parsed", max_length=50,default=None, null=True)
    hash = models.CharField(
        max_length=32,
        help_text="MD5 hash generated from request properties",
        unique=True,
    )
    created_at = models.DateTimeField(
        help_text="The time at which the database record was created (!=session_start)=",
        auto_now_add=True,
    )

    objects = UserVisitManager()

    class Meta:
        get_latest_by = "session_start"

    def __str__(self) -> str:
        return f"{self.user} visited the site on {self.session_start}"

    def __repr__(self) -> str:
        return f"<UserVisit id={self.id} user_id={self.user_id} date='{self.date}'>"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Set hash property and save object."""
        self.hash = self.md5()
        super().save(*args, **kwargs)
	
    def parse_agent(self, ua) -> str:
        agent = user_agents.parsers.parse(ua)
        return f"{agent.get_browser} - {agent.get_device} - {agent.get_os}"

    @property
    def user_agent(self) -> user_agents.parsers.UserAgent:
        """Return UserAgent object from the raw user_agent string."""
        return user_agents.parsers.parse(self.ua_string)

    @property
    def date(self) -> datetime.date:
        """Extract the date of the visit from the session_start."""
        return self.session_start.date()

    def md5(self) -> str:
        """Generate MD5 hash used to identify duplicate visits."""
        h = hashlib.md5()  # Create a new MD5 hash object
        h.update(str(self.user.id).encode('utf-8'))  # Encode user ID
        h.update(self.date.isoformat().encode('utf-8'))  # Encode date
        h.update(self.session_key.encode('utf-8'))  # Encode session key
        h.update(self.remote_addr.encode('utf-8'))  # Encode remote address
        h.update(self.ua_string.encode('utf-8'))  # Encode user agent string
        return h.hexdigest()  # Retu


@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
	# Delete all other sessions for the user
	Session.objects.filter(usersession__user=user).delete()

	# Save the current session
	request.session.save()

	# Create a new UserSession for the current session
	UserSession.objects.get_or_create(user=user,session_id=request.session.session_key)

	# Get or create UserVisit for the current session
	user_visit, created = UserVisit.objects.get_or_create(
		session_key=request.session.session_key,
		defaults={
			'user': user,
			'session_start': timezone.now(),
			'session_end': request.session.get_expiry_date()
		}
	)
	if not created:
		user_visit.session_end = request.session.get_expiry_date()
		user_visit.save()

@receiver(user_logged_out)
def change_session_end(sender, request, **kwargs):
	uv = UserVisit.objects.filter(user = request.user).latest()
	uv.session_end = timezone.now()
	uv.save()

