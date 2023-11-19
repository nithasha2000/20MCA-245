import json
import random
from api.utilities import email_utils, response_utils
from base.models import Login, CompanyRegister, JobSeekerRegister
from api.utilities.validation_utils import ValidateUtil
from base.models import Login, CompanyRegister, JobSeekerRegister, JobPost
from base.serializers import (
    loginSerializer, 
    CompanyRegisterSerializer, 
    JobSeekerRegisterSerializer, 
    JobPostSerializer,
    UserNotificationSerializer)
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

    def dashboard_sidebar_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('email', ''))
                if login_db_data.role == request.get("role", ''):
                    method_obj = getattr(response_utils, f"{request.get('role', '')}_sidebar")
                    response_json["message"] = "success"
                    response_json["data"] = method_obj()
                else:
                    response_json["data"] = "Account verification failed"
            except ObjectDoesNotExist:
                response_json["data"] = "Account doesnot exist"
        except Exception as e:
            print(f'Exception occured in fetching sidebar: {e}')
        return response_json
    
    def forgot_password_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('email', ''))
                if login_db_data:
                    otp = ''.join(random.choice('0123456789') for _ in range(6))
                    users.update({request.get('email', ''): {'otp': otp}})
                    sub=f"Password Reset"
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
    
    def job_post_create_handler(request, request_data, response_json):
        try:
            try:
                user_data_obj = request.POST.get("user_data", {})
                user_data = json.loads(user_data_obj)
                valid, validate_resp = ValidateUtil.job_post_validate(request_data)
                if not valid:
                    response_json["data"] = validate_resp
                    return response_json
                job_post_data = {
                    "job_title": request_data.get("job_title", ''),
                    "job_description": request_data.get("job_description", ''),
                    "experience": request_data.get("experience", ''),
                    "location": request_data.get("location", ''),
                    "salary_range": request_data.get("salary_range", ''),
                    "application_deadline": request_data.get("application_deadline", '')
                }
                login_db_data = Login.objects.get(username=user_data.get('username', ''), is_deleted=0)
                if login_db_data:
                    if login_db_data.role == user_data.get("role", "") and login_db_data.role == "company":
                        job_post_data["user"] = login_db_data.user_id
                        job_post_serializer = JobPostSerializer(data=job_post_data)
                        if job_post_serializer.is_valid():
                            job_post_serializer.save()
                            response_json["message"] = "success"
                        else:
                            response_json["data"] = "Not able to create new job post"
                    else:
                        response_json["data"] = "Your are not authorized to view this page"  
                else:
                    response_json["data"] = "Your are not authorized to view this page"  
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in job_post_create_handler: {e}')
        return response_json

    def job_post_edit_handler(request, request_data, response_json):
        try:
            try:
                user_data_obj = request.POST.get("user_data", {})
                user_data = json.loads(user_data_obj)
                valid, validate_resp = ValidateUtil.job_post_validate(request_data)
                if not valid:
                    response_json["data"] = validate_resp
                    return response_json
                job_post_data = {
                    "job_title": request_data.get("job_title", ''),
                    "job_description": request_data.get("job_description", ''),
                    "experience": request_data.get("experience", ''),
                    "location": request_data.get("location", ''),
                    "salary_range": request_data.get("salary_range", ''),
                    "application_deadline": request_data.get("application_deadline", '')
                }
                login_db_data = Login.objects.get(username=user_data.get('username', ''), is_deleted=0)
                if login_db_data:
                    if login_db_data.role == user_data.get("role", "") and login_db_data.role == "company":
                        job_post_data["user"] = login_db_data.user_id
                        job_data = JobPost.objects.get(job_post_id=request_data.get("job_post_id", ""))
                        if job_data:
                            job_data.job_title = job_post_data["job_title"]
                            job_data.job_description = job_post_data["job_description"]
                            job_data.experience = job_post_data["experience"]
                            job_data.location = job_post_data["location"]
                            job_data.salary_range = job_post_data["salary_range"]
                            job_data.application_deadline = job_post_data["application_deadline"]
                            # Save the changes
                            job_data.save()
                            response_json["message"] = "success"
                        else:
                            response_json["data"] = "Not able to edit job post"
                    else:
                        response_json["data"] = "Your are not authorized to view this page"  
                else:
                    response_json["data"] = "Your are not authorized to view this page"  
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in job_post_edit_handler: {e}')
        return response_json

    def job_post_delete_handler(request, request_data, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request_data.get('username', ''), is_deleted=0)
                if login_db_data:
                    if login_db_data.role == request_data.get("role", "") and login_db_data.role == "company":
                        job_data = JobPost.objects.get(job_post_id=request_data.get("job_post_id", ""))
                        if job_data:
                            job_data.delete()
                            response_json["message"] = "success"
                        else:
                            response_json["data"] = "Not able to edit job post"
                    else:
                        response_json["data"] = "Your are not authorized to view this page"  
                else:
                    response_json["data"] = "Your are not authorized to view this page"  
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in job_post_delete_handler: {e}')
        return response_json

    def view_job_list_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                if login_db_data:
                    if login_db_data.role == request.get("role", "") and login_db_data.role == "company":
                        job_post_data = JobPost.objects.filter(user=login_db_data.user_id)
                        company_data = CompanyRegister.objects.get(user=login_db_data.user_id)
                        job_post_serializer = JobPostSerializer(job_post_data, many=True)
                        if job_post_data:
                            for job_post_record in job_post_serializer.data:
                                job_post_record["company_name"] = company_data.company_name
                            response_json["message"] = "success"
                            response_json["data"] = job_post_serializer.data
                        else:
                            response_json["message"] = "success"
                    elif login_db_data.role == request.get("role", "") and login_db_data.role == "job_seeker":
                        job_post_data = JobPost.objects.filter(user=login_db_data.user_id)
                        company_data = CompanyRegister.objects.get(user=login_db_data.user_id)
                        job_post_serializer = JobPostSerializer(job_post_data, many=True)
                        if job_post_data:
                            for job_post_record in job_post_serializer.data:
                                job_post_record["company_name"] = company_data.company_name
                            response_json["message"] = "success"
                            response_json["data"] = job_post_serializer.data
                        else:
                            response_json["message"] = "success"
                    else:
                        response_json["data"] = "Your are not authorized to view this page"
                else:
                    response_json["data"] = "Your are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in view job list: {e}')
        return response_json