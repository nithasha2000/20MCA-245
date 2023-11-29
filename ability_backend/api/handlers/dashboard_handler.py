from datetime import date
import json
import random
import zlib

from api.utilities import email_utils, response_utils
from base.models import Login, CompanyRegister, JobSeekerRegister
from api.utilities.validation_utils import ValidateUtil
from base.models import Login, CompanyRegister, JobSeekerRegister, JobPost, JobApplications, SaveJobPosts
from base.serializers import (
    loginSerializer, 
    CompanyRegisterSerializer, 
    JobSeekerRegisterSerializer, 
    JobPostSerializer,
    JobApplicationsSerializer,
    SaveJobPostsSerializer,
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
                        job_post_data["post_status"] = "opened"
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
    
    def job_post_status_handler(request, request_data, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request_data.get('username', ''), is_deleted=0)
                today_date = date.today()
                if login_db_data:
                    if login_db_data.role == request_data.get("role", "") and login_db_data.role == "company":
                        job_data = JobPost.objects.get(job_post_id=request_data.get("job_post_id", ""))
                        if job_data:
                            if job_data.post_status == "opened":
                                job_data.post_status = "closed"
                                job_data.save()
                                response_json["message"] = "success"
                            else:
                                if job_data.application_deadline >= today_date:
                                    job_data.post_status = "opened"
                                    job_data.save()
                                    response_json["message"] = "success"
                                else:
                                    response_json["data"] = "Update application deadline"
                        else:
                            response_json["data"] = "Not able to edit job post"
                    else:
                        response_json["data"] = "Your are not authorized to view this page"  
                else:
                    response_json["data"] = "Your are not authorized to view this page"  
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in job_post_status_handler: {e}')
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
                role = request.get("role", "")

                if login_db_data:
                    if login_db_data.role == role:
                        if role == "company":
                            job_post_data = JobPost.objects.filter(user=login_db_data.user_id)
                            company_data = CompanyRegister.objects.get(user=login_db_data.user_id)
                        elif role == "job_seeker":
                            job_post_data = JobPost.objects.all()
                            company_data = None

                        job_post_serializer = JobPostSerializer(job_post_data, many=True)

                        if job_post_serializer.data:
                            for job_post_record in job_post_serializer.data:
                                if company_data:
                                    job_post_record["company_name"] = company_data.company_name
                                else:
                                    company_data = CompanyRegister.objects.get(user=job_post_record["user"])
                                    if company_data:
                                        job_post_record["company_name"] = company_data.company_name

                            response_json["message"] = "success"
                            response_json["data"] = job_post_serializer.data
                        else:
                            response_json["message"] = "success"
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"

            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in view job list: {e}')
        return response_json
    
    def apply_job_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                job_post_id = request.get("job_post_id", "")
                application_data = {}
                today_date = date.today()
                
                if login_db_data or login_db_data.role != "job_seeker":
                    job_post_data = JobPost.objects.get(job_post_id=job_post_id)

                    job_application = JobApplications.objects.filter(job_post=job_post_id, user=login_db_data.user_id)
                    if job_application:
                        response_json["data"] = "Already applied"
                        return response_json
                    if job_post_data.post_status == "closed":
                        response_json["data"] = "Cannot Apply! Job Closed"
                        return response_json
                    
                    if today_date <= job_post_data.application_deadline:
                        
                        if job_post_data:
                            application_data.update({"user": login_db_data.user_id, "job_post": job_post_id})
                            application_data.update({"application_status": "applied"})

                            job_applications_serializer = JobApplicationsSerializer(data=application_data)
                            if job_applications_serializer.is_valid():
                                job_applications_serializer.save()
                                response_json["message"] = "success"
                            else:
                                response_json["data"] = ""
                        else:
                            response_json["data"] = ""
                    else:
                        response_json["data"] = "Application date is over!"
                else:
                    response_json["data"] = "You are not authorized to view this page"

            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in apply_job_handler: {e}')
        return response_json
    
    def unapply_job_handler(request_data, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request_data.get('username', ''), is_deleted=0)
                if login_db_data:
                    if login_db_data.role == request_data.get("role", "") and login_db_data.role == "job_seeker":
                        applied_post = request_data.get("applied_post", [])
                        job_application_data = JobApplications.objects.get(job_applications_id=applied_post.get("job_applications_id", ""))
                        if job_application_data:
                            job_application_data.delete()
                            response_json["message"] = "success"
                        else:
                            response_json["data"] = "Not able to delete job application"
                    else:
                        response_json["data"] = "Your are not authorized to view this page"  
                else:
                    response_json["data"] = "Your are not authorized to view this page"  
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in unapply_job_handler: {e}')
        return response_json
    
    def save_job_post_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                job_post_id = request.get("job_post_id", "")
                application_data = {}

                if login_db_data or login_db_data.role != "job_seeker":
                    job_post_data = JobPost.objects.filter(job_post_id=job_post_id)
                    job_post_serializer = JobPostSerializer(job_post_data, many=True)

                    save_job = SaveJobPosts.objects.filter(job_post=job_post_id)
                    if save_job:
                        response_json["data"] = "Already saved"
                        return response_json

                    if job_post_serializer.data:
                        application_data.update({"user": login_db_data.user_id, "job_post": job_post_id})

                        save_job_post_serializer = SaveJobPostsSerializer(data=application_data)
                        if save_job_post_serializer.is_valid():
                            save_job_post_serializer.save()
                            response_json["message"] = "success"
                        else:
                            response_json["data"] = ""
                    else:
                        response_json["data"] = ""
                else:
                    response_json["data"] = "You are not authorized to view this page"

            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in save_job_post_handler: {e}')
        return response_json
    
    def view_save_job_post_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                role = request.get("role", "")
                job_list = []
                if login_db_data:
                    if login_db_data.role == role and role == 'job_seeker':
                        saved_job_post_data = SaveJobPosts.objects.filter(user=login_db_data.user_id)

                        saved_job_post_serializer = SaveJobPostsSerializer(saved_job_post_data, many=True)

                        if saved_job_post_serializer.data:
                            job_post_ids = [record["job_post"] for record in saved_job_post_serializer.data]

                            job_posts = JobPost.objects.filter(job_post_id__in=job_post_ids)

                            for job_post in job_posts:
                                job_post_serializer = JobPostSerializer(job_post)
                                if job_post_serializer.data:
                                    company_data = CompanyRegister.objects.get(user=job_post_serializer.data["user"])
                                    if company_data:
                                        updated_job_data = job_post_serializer.data.copy()
                                        updated_job_data["company_name"] = company_data.company_name
                                        updated_job_data["save_post"] = saved_job_post_serializer.data
                                        job_list.append(updated_job_data)
                            response_json["message"] = "success"
                            response_json["data"] = job_list
                        else:
                            response_json["message"] = "success"
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"

            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in view_save_job_post_handler: {e}')
        return response_json
    
    def unsave_job_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                save_post_id = request.get("save_post", [])[0].get("save_job_id", "")
                
                if login_db_data or login_db_data.role != "job_seeker":
                    save_job = SaveJobPosts.objects.get(save_job_id=save_post_id)
                    if save_job:
                        save_job.delete()
                        response_json["message"] = "success"
                    else:
                        response_json["data"] = "Something went wrong"
                else:
                    response_json["data"] = "You are not authorized to view this page"

            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in unsave_job_handler: {e}')
        return response_json
    
    def applied_job_list_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                role = request.get("role", "")
                job_list = []
                if login_db_data:
                    if login_db_data.role == role and role == 'job_seeker':
                        applied_job_post_data = JobApplications.objects.filter(user=login_db_data.user_id)
                        applied_job_post_serializer = JobApplicationsSerializer(applied_job_post_data, many=True)
                        if applied_job_post_serializer.data:
                            job_post_ids = [record["job_post"] for record in applied_job_post_serializer.data]
                            job_posts = JobPost.objects.filter(job_post_id__in=job_post_ids)
                            for job_post in job_posts:
                                job_post_serializer = JobPostSerializer(job_post)
                                if job_post_serializer.data:
                                    company_data = CompanyRegister.objects.get(user=job_post_serializer.data["user"])
                                    if company_data:
                                        updated_job_data = job_post_serializer.data.copy()
                                        updated_job_data["company_name"] = company_data.company_name
                                        for applied_job in applied_job_post_serializer.data:
                                            if applied_job["job_post"] == job_post.job_post_id:
                                                updated_job_data["applied_post"] = applied_job
                                        job_list.append(updated_job_data)
                            response_json["message"] = "success"
                            response_json["data"] = job_list
                        else:
                            response_json["message"] = "success"
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in applied_job_list_handler: {e}')
        return response_json
    
    def view_applicants_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                role = request.get("role", "")
                job_post_id = request.get("job_post_id", "")
                job_applicants = []
                if login_db_data:
                    if login_db_data.role == role and login_db_data.role == "company":
                        job_applications_data = JobApplications.objects.filter(job_post_id=job_post_id)
                        job_applicants_serializer = JobApplicationsSerializer(job_applications_data, many=True)
                        if job_applicants_serializer.data:
                            for job_applicants_record in job_applicants_serializer.data:
                                job_seeker_data = JobSeekerRegister.objects.get(user=job_applicants_record["user"])
                                job_seeker_serializer = JobSeekerRegisterSerializer(job_seeker_data)
                                if job_seeker_serializer.data:
                                    job_seekers = job_seeker_serializer.data
                                    user_data = Login.objects.get(user_id=job_seekers["user"])
                                    user_data_serializer = loginSerializer(user_data)
                                    job_seekers["email"] = user_data_serializer.data["username"]
                                    job_seekers["status"] = job_applicants_record["application_status"]
                                    job_applicants.append(job_seekers)
                            response_json["message"] = "success"
                            response_json["data"] = job_applicants
                        else:
                            response_json["message"] = "success"
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in view_applicants_handler: {e}')
        return response_json
    
    def download_applicant_resume_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                role = request.get("role", "")
                job_seeker_id = request.get("job_seeker_id", "")
                response = ""
                if login_db_data:
                    if login_db_data.role == role and login_db_data.role == "company":
                        job_seeker_data = JobSeekerRegister.objects.get(job_seeker_id=job_seeker_id)
                        job_seeker_serializer = JobSeekerRegisterSerializer(job_seeker_data)
                        if job_seeker_serializer.data:
                            job_seekers = job_seeker_serializer.data
                            try:
                                with open(job_seekers["resume"], 'rb') as resume_file:
                                    response = (resume_file.read())
                                    compressed_data = zlib.compress(response)
                                    response_json["message"] = "success"
                                    response_json["data"] = compressed_data
                                if not response:
                                    response_json["data"] = "Loading resume failed"
                            except Exception as e:
                                response_json["data"] = "Loading resume failed"
                        else:
                            response_json["message"] = "success"
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in download_applicant_resume_handler: {e}')
        return response_json
    
    def shortlist_candidate_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                role = request.get("role", "")
                job_seeker_id = request.get("job_seeker_id", "")
                job_post_id = request.get("job_id", "")
                if login_db_data:
                    if login_db_data.role == role and role == 'company':
                        job_post_data = JobApplications.objects.get(user=job_seeker_id, job_post=job_post_id)
                        job_seeker_data = Login.objects.get(user_id=job_seeker_id, is_deleted=0)
                        if job_post_data.application_status == "applied":
                            job_post_data.application_status = "shortlisted"
                            sub=f"Job Shortlisted"
                            email_body = f"Hai {job_seeker_data.username} your resume has been shorlisted for a job"
                            email_html_path = r"D:\20MCA-245\ability-project\20MCA-245\ability_backend\api\utilities\link_email.html"
                            email_utils.send_welcome_email_in_background(job_seeker_data.username, sub, email_body, email_html_path)
                        elif job_post_data.application_status == "shortlisted":
                            job_post_data.application_status = "rejected"
                        job_post_data.save()
                        response_json["message"] = "success"
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in shortlist_candidate_handler: {e}')
        return response_json