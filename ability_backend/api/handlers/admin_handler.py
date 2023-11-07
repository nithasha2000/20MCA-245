from base.models import Login, CompanyRegister, JobSeekerRegister
from base.serializers import loginSerializer, CompanyRegisterSerializer, JobSeekerRegisterSerializer
from django.core.exceptions import ObjectDoesNotExist
class AdminHandler:
    def view_users(request, response_json):
        try:
            try:
                if request.get("role") == "admin":
                    users = []
                    company_register_data = CompanyRegister.objects.all()
                    company_serializer = CompanyRegisterSerializer(company_register_data, many=True)
                    for company_record in company_serializer.data:
                        try:
                            login_db_data = Login.objects.get(username=company_record['email'], is_deleted=0)
                            
                            if login_db_data:
                                company_record['role'] = login_db_data.role
                        except ObjectDoesNotExist:
                            continue
                    users.extend(company_serializer.data)
                    job_seeker_register_data = JobSeekerRegister.objects.all()
                    job_seeker_serializer = JobSeekerRegisterSerializer(job_seeker_register_data, many=True)
                    for job_seeker in job_seeker_serializer.data:
                        try:
                            login_db_data = Login.objects.get(username=job_seeker['email'], is_deleted=0)
                            
                            if login_db_data:
                                job_seeker['role'] = login_db_data.role
                        except ObjectDoesNotExist:
                            continue
                    users.extend(job_seeker_serializer.data)
                    print(users)
                    response_json["message"] = "success"
                    response_json["data"] = users
                else:
                    response_json["data"] = "Your are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in view users: {e}')
        return response_json