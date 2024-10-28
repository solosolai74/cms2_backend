from exam.models import  ExamDetails,ExamCenter

def validateexamceter(exam,center):
    resdata = {}
    try:
        examcode =  ExamDetails.objects.get(examcode=exam,isactive=True)
        centercode = ExamCenter.objects.get(centercode = center,examcode=examcode)
        print(centercode,"=-=")
        resdata = {
            'status' : True,
            'examobject' :examcode,
            'centerobj' : centercode,
        }
        return resdata
    
    except Exception as e:
       print("Exeption in exam center get object: " + str(e))
       resdata = {
          'status' : False,
          'message' : 'Exam Center Detils is Not Available',
          'error' : str(e)
       }
       return resdata
    

    
