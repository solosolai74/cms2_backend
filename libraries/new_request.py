from datetime import datetime
from exam.models import ExamCenterRequest

def CreateRequestStatus(examcode,centercode,request_type,request_priority,ipaddress,requesttime = datetime.today()):
                        
    try:
        '''
            Insert request entry
        '''
        ruquestobj = ExamCenterRequest.objects.filter(examcode=examcode,centercode=centercode,requesttime=requesttime)
        if ruquestobj.count():
        #   ruquestobj.update()
          print("YES Request is available")
        else:
            ExamCenterRequest.objects.create(examcode=examcode,centercode=centercode,request_type=request_type,request_priority=request_priority,remote_address=ipaddress,requesttime=requesttime)
          
    except Exception as details:
        print("Issues in create or upate in request string %s" % details)
    return True
