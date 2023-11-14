import random
from api.utilities import email_utils
from base.models import Login, CompanyRegister, JobSeekerRegister
from base.serializers import loginSerializer, CompanyRegisterSerializer, JobSeekerRegisterSerializer, UserNotificationSerializer
from django.core.exceptions import ObjectDoesNotExist

users = {}
class DashBoardHandler:
    def view_users(request, response_json):
        try:
            try:
                if request.get("role") == "admin":
                    users = []
                    company_register_data = CompanyRegister.objects.all()
                    company_serializer = CompanyRegisterSerializer(company_register_data, many=True)
                    for company_record in company_serializer.data:
                        try:
                            login_db_data = Login.objects.get(user_id=company_record['user'])
                            
                            if login_db_data:
                                company_record["email"] = login_db_data.username
                                company_record["role"] = login_db_data.role
                                company_record["is_deleted"] = login_db_data.is_deleted
                        except ObjectDoesNotExist:
                            continue
                    users.extend(company_serializer.data)
                    job_seeker_register_data = JobSeekerRegister.objects.all()
                    job_seeker_serializer = JobSeekerRegisterSerializer(job_seeker_register_data, many=True)
                    for job_seeker in job_seeker_serializer.data:
                        try:
                            login_db_data = Login.objects.get(user_id=job_seeker['user'])
                            
                            if login_db_data:
                                job_seeker["email"] = login_db_data.username
                                job_seeker['role'] = login_db_data.role
                                job_seeker["is_deleted"] = login_db_data.is_deleted
                        except ObjectDoesNotExist:
                            continue
                    users.extend(job_seeker_serializer.data)
                    response_json["message"] = "success"
                    response_json["data"] = users
                else:
                    response_json["data"] = "Your are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in view users: {e}')
        return response_json
    
    def account_activation_handler(request, response_json):
        try:
            try:
                if request.get("role") == "admin":
                    try:
                        login_db_data = Login.objects.get(username=request.get('change_username', ''))
                        message = ""
                        if login_db_data:
                            if login_db_data.is_deleted:
                                login_db_data.is_deleted = 0
                                message = "activated"
                            else:
                                login_db_data.is_deleted = 1
                                message = "deactivated"
                            login_db_data.save()
                            sub=f"Account Activation"
                            email_body = f"Hai {request.get('change_username', '')} your account has been {message}"
                            email_html_path = r"D:\20MCA-245\ability-project\20MCA-245\ability_backend\api\utilities\link_email.html"
                            email_utils.send_welcome_email_in_background(request.get('change_username', ''), sub, email_body, email_html_path)
                            response_json["message"] = "success"
                    except ObjectDoesNotExist:
                        response_json["data"] = "Account does not exist"
                else:
                    response_json["data"] = "Your are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in activating users account: {e}')
        return response_json
    
    def forgot_password_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('email', ''))
                if login_db_data:
                    otp = ''.join(random.choice('0123456789') for _ in range(6))
                    users.update({request.get('email', ''): {'otp': otp}})
                    sub=f"Account Activation"
                    email_body = f"Hai {request.get('email', '')} <br> This is your otp to reset your account {otp}"
                    email_html_path = r"D:\20MCA-245\ability-project\20MCA-245\ability_backend\api\utilities\link_email.html"
                    email_utils.send_welcome_email_in_background(request.get('email', ''), sub, email_body, email_html_path)
                    response_json["message"] = "success"
            except ObjectDoesNotExist:
                response_json["data"] = "Account doesnot exist"
        except Exception as e:
            print(f'Exception occured in forgot password: {e}')
        return response_json
    
    def verify_otp_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('email', ''))
                if login_db_data:
                    login_serializer = loginSerializer(instance=login_db_data)
                    if request.get('otp', '') == users.get(request.get('email', '')).get('otp'):
                        response_json["message"] = "success"
                        response_json["data"] = login_serializer.data
                        users.update({request.get('email', ''): {'otp': ""}})
                    else:
                        response_json["data"] = "Invalid OTP"
            except ObjectDoesNotExist:
                response_json["data"] = "Account doesnot exist"
        except Exception as e:
            print(f'Exception occured in forgot password: {e}')
        return response_json
    

    def view_notifications(request, response_json):
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
                                company_record["email"] = login_db_data.email
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
            print(f'Exception occured in view notifications: {e}')
        return response_json