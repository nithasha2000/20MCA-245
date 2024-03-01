import ast
from datetime import date
import json
import random
import zlib
from django.db.models import Q
from api.utilities import email_utils, response_utils
from api.utilities.validation_utils import ValidateUtil
from base.models import EmployeeRegister, Login, CompanyRegister, JobSeekerRegister, JobPost, JobApplications, SaveJobPosts, UserNotifications, ExamForm, ExamQuestions
from base.serializers import (
    EmployeeRegisterSerializer,
    loginSerializer, 
    CompanyRegisterSerializer, 
    JobSeekerRegisterSerializer, 
    JobPostSerializer,
    JobApplicationsSerializer,
    SaveJobPostsSerializer,
    UserNotificationSerializer,
    ExamFormSerializer,
    ExamQuestionSerializer)
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
                    employee_register_data = EmployeeRegister.objects.all()
                    employee_serializer = EmployeeRegisterSerializer(employee_register_data, many=True)
                    for employee in employee_serializer.data:
                        try:
                            login_db_data = Login.objects.get(user_id=employee['user'])
                            
                            if login_db_data:
                                employee["email"] = login_db_data.username
                                employee['role'] = login_db_data.role
                                employee["is_deleted"] = login_db_data.is_deleted
                        except ObjectDoesNotExist:
                            continue
                    users.extend(employee_serializer.data)
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
                notification_list = []
                login_db_data = Login.objects.get(username=request.get('username', ''))
                if login_db_data:
                    if login_db_data.role == "admin" and request.get("role", "") == "admin":
                        notification_types = ["registration", "job_post_approval"]
                        for notification_type in notification_types:
                            notifications_data = UserNotifications.objects.filter(type=notification_type, viewed=0).values()
                            notification_list.extend(notifications_data)
                        response_json["message"] = "success"
                        response_json["data"] = notification_list
                        response_json["count"] = len(notification_list)
                    if login_db_data.role == "company" and request.get("role", "") == "company":
                        notification_types = ["job_post", "job_post_apply"]
                        for notification_type in notification_types:
                            notifications_data = UserNotifications.objects.filter(user=login_db_data.user_id, type=notification_type, viewed=0).values()
                            notification_list.extend(notifications_data)
                        response_json["message"] = "success"
                        response_json["data"] = notification_list
                        response_json["count"] = len(notification_list)
                    if login_db_data.role == "job_seeker" and request.get("role", "") == "job_seeker":
                        notification_types = ["job_post_applied"]
                        for notification_type in notification_types:
                            notifications_data = UserNotifications.objects.filter(user=login_db_data.user_id, type=notification_type, viewed=0).values()
                            notification_list.extend(notifications_data)
                        response_json["message"] = "success"
                        response_json["data"] = notification_list
                        response_json["count"] = len(notification_list)
                    if login_db_data.role == "employee" and request.get("role", "") == "employee":
                        notification_types = []
                        for notification_type in notification_types:
                            notifications_data = UserNotifications.objects.filter(user=login_db_data.user_id, type=notification_type, viewed=0).values()
                            notification_list.extend(notifications_data)
                        response_json["message"] = "success"
                        response_json["data"] = notification_list
                        response_json["count"] = len(notification_list)
            except ObjectDoesNotExist:
                response_json["data"] = "Account doesnot exist"
        except Exception as e:
            print(f'Exception occured in view_notifications: {e}')
        return response_json
    
    def mark_notifications_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''))
                if login_db_data:
                    if login_db_data.role == request.get("role", ""):
                        notifications_data = UserNotifications.objects.get(notification_id=request.get("notification_id", ""))
                        notifications_data.viewed = 1
                        notifications_data.save()
                        response_json["message"] = "success"
            except ObjectDoesNotExist:
                response_json["data"] = "Account doesnot exist"
        except Exception as e:
            print(f'Exception occured in mark_notifications_handler: {e}')
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
                    "soft_skills": json.loads(request.POST.get("soft_skills", {})),
                    "salary_range": request_data.get("salary_range", ''),
                    "application_deadline": request_data.get("application_deadline", '')
                }
                notification = {
                    "notification": f"New Job Post created for {request_data.get('job_title', '')} wait for approval",
                    "type": "job_post",
                    "viewed": 0
                }
                notification_admin = {
                    "notification": f"New Job Post created for {request_data.get('job_title', '')} by {user_data.get('username', '')} waiting for approval",
                    "type": "job_post_approval",
                    "viewed": 0
                }
                login_db_data = Login.objects.get(username=user_data.get('username', ''), is_deleted=0)
                if login_db_data:
                    if login_db_data.role == user_data.get("role", "") and login_db_data.role == "company":
                        job_post_data["user"] = login_db_data.user_id
                        job_post_data["post_status"] = "opened"
                        job_post_data["approval"] = 0
                        notification["user"] = login_db_data.user_id
                        notification_admin["user"] = login_db_data.user_id
                        job_post_serializer = JobPostSerializer(data=job_post_data)
                        notification_serializer = UserNotificationSerializer(data=notification)
                        if job_post_serializer.is_valid():
                            job_post_serializer.save()
                            if notification_serializer.is_valid():
                                notification_serializer.save()
                                notification_serializer_new = UserNotificationSerializer(data=notification_admin)
                                if notification_serializer_new.is_valid():
                                    notification_serializer_new.save()
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
                    "soft_skills": json.loads(request.POST.get("soft_skills", {})),
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
                            job_data.set_soft_skills(job_post_data["soft_skills"])
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
                            job_post_data = JobPost.objects.filter(approval=1)
                            company_data = None
                        elif role == "admin":
                            job_post_data = JobPost.objects.filter()
                            company_data = None

                        job_post_serializer = JobPostSerializer(job_post_data, many=True)

                        if job_post_serializer.data:
                            for job_post_record in job_post_serializer.data:
                                try:
                                    job_post_record["soft_skills"] = json.loads(job_post_record["soft_skills"])
                                except json.JSONDecodeError:
                                    job_post_record["soft_skills"] = ast.literal_eval(job_post_record["soft_skills"])
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
                response_json["message"] = "success"
        except Exception as e:
            print(f'Exception occured in view job list: {e}')
        return response_json
    
    def job_post_filter_handler(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                filter_data = request.get("filterData", "")
                role = request.get("role", "")
                search_value = request.get("search_value", "")
                if login_db_data:
                    if login_db_data.role == role:
                        if role == "company":
                            job_post_data = JobPost.objects.filter(
                                Q(job_title__icontains=search_value) |
                                Q(job_description__icontains=search_value) |
                                Q(experience__icontains=search_value) |
                                Q(salary_range__icontains=search_value) |
                                Q(location__icontains=search_value) |
                                Q(user__companyregister__company_name__icontains=search_value),
                                user=login_db_data.user_id
                            )
                            company_data = CompanyRegister.objects.get(user=login_db_data.user_id)
                        elif role == "job_seeker":
                            job_post_data = JobPost.objects.filter(
                                Q(job_title__icontains=search_value) |
                                Q(job_description__icontains=search_value) |
                                Q(experience__icontains=search_value) |
                                Q(salary_range__icontains=search_value) |
                                Q(location__icontains=search_value) |
                                Q(user__companyregister__company_name__icontains=search_value),
                                approval=1)
                            company_data = None
                        elif role == "admin":
                            job_post_data = JobPost.objects.filter(
                                Q(job_title__icontains=search_value) |
                                Q(job_description__icontains=search_value) |
                                Q(experience__icontains=search_value) |
                                Q(salary_range__icontains=search_value) |
                                Q(location__icontains=search_value) |
                                Q(user__companyregister__company_name__icontains=search_value),
                            )
                            company_data = None
                        if filter_data:
                            job_post_data = job_post_data.filter(
                                Q(job_title__icontains=filter_data.get('job_title', '')) &
                                Q(location__icontains=filter_data.get('location', '')) &
                                Q(salary_range__icontains=filter_data.get('salary_range', ''))
                            )

                            # Handle soft_skills filter separately
                            soft_skills_filter = filter_data.get('soft_skills', '')
                            if soft_skills_filter:
                                job_post_data = job_post_data.filter(Q(soft_skills__icontains=f'"{soft_skills_filter}": True')|
                                                                     Q(soft_skills__icontains=f"'{soft_skills_filter}': True"))

                        job_post_serializer = JobPostSerializer(job_post_data, many=True)

                        if job_post_serializer.data:
                            for job_post_record in job_post_serializer.data:
                                try:
                                    job_post_record["soft_skills"] = json.loads(job_post_record["soft_skills"])
                                except json.JSONDecodeError:
                                    job_post_record["soft_skills"] = ast.literal_eval(job_post_record["soft_skills"])
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
                response_json["message"] = "success"
        except Exception as e:
            print(f'Exception occured in job_post_filter_handler: {e}')
        return response_json
    
    def job_post_approve_handler(request_data, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request_data.get('username', ''), is_deleted=0)
                if login_db_data:
                    if login_db_data.role == request_data.get("role", "") and login_db_data.role == "admin":
                        job_data = JobPost.objects.get(job_post_id=request_data.get("job_post_id", ""))
                        if job_data:
                            if job_data.approval == 0 and request_data.get("status", "") == "approve":
                                job_data.approval = 1
                                job_data.save()
                                notification = {
                                    "notification": f"Job Post Approved for {job_data.job_title}",
                                    "type": "job_post",
                                    "viewed": 0
                                }
                                response_json["message"] = "success"
                            if job_data.approval == 0 and request_data.get("status", "") == "reject":
                                job_data.approval = 2
                                job_data.save()
                                notification = {
                                    "notification": f"Job Post Rejected for {job_data.job_title}",
                                    "type": "job_post",
                                    "viewed": 0
                                }
                                response_json["message"] = "success"
                            if job_data.approval == 1 and request_data.get("status", "") == "approve":
                                response_json["data"] = "Already approved"
                            if job_data.approval == 2 and request_data.get("status", "") == "reject":
                                response_json["data"] = "Already rejected"
                            if job_data.approval == 2 and request_data.get("status", "") == "approve":
                                job_data.approval = 1
                                job_data.save()
                                notification = {
                                    "notification": f"Job Post Approved for {job_data.job_title}",
                                    "type": "job_post",
                                    "viewed": 0
                                }
                                response_json["message"] = "success"
                            if notification:
                                notification["user"] = job_data.user_id
                                notification_serializer = UserNotificationSerializer(data=notification)
                                if notification_serializer.is_valid():
                                    notification_serializer.save()
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
                            notification = {
                                "notification": f"{login_db_data.username} Applied for {job_post_data.job_title}",
                                "type": "job_post_apply",
                                "viewed": 0
                            }
                            notification_new = {
                                "notification": f"Applied for {job_post_data.job_title}",
                                "type": "job_post_applied",
                                "viewed": 0
                            }
                            notification["user"] = job_post_data.user_id
                            notification_new["user"] = login_db_data.user_id
                            notification_serializer = UserNotificationSerializer(data=notification)
                            job_applications_serializer = JobApplicationsSerializer(data=application_data)
                            if job_applications_serializer.is_valid():
                                job_applications_serializer.save()
                                if notification_serializer.is_valid():
                                    notification_serializer.save()
                                    notification_serializer = UserNotificationSerializer(data=notification_new)
                                    if notification_serializer.is_valid():
                                        notification_serializer.save()
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
                                        try:
                                            updated_job_data["soft_skills"] = json.loads(updated_job_data["soft_skills"])
                                        except json.JSONDecodeError:
                                            updated_job_data["soft_skills"] = ast.literal_eval(updated_job_data["soft_skills"])
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
                                        try:
                                            updated_job_data["soft_skills"] = json.loads(updated_job_data["soft_skills"])
                                        except json.JSONDecodeError:
                                            updated_job_data["soft_skills"] = ast.literal_eval(updated_job_data["soft_skills"])
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
    
    def apply_job_post_filter_handler(request, response_json):
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
                            filter_data = request.get("filterData", "")
                            search_value = request.get("search_value", "")
                            if search_value:
                                job_posts = job_posts.filter(
                                    Q(job_title__icontains=search_value) |
                                    Q(job_description__icontains=search_value) |
                                    Q(experience__icontains=search_value) |
                                    Q(salary_range__icontains=search_value) |
                                    Q(location__icontains=search_value) |
                                    Q(user__companyregister__company_name__icontains=search_value)
                                )
                            if filter_data:
                                job_posts = job_posts.filter(
                                    Q(job_title__icontains=filter_data.get('job_title', '')) &
                                    Q(location__icontains=filter_data.get('location', '')) &
                                    Q(salary_range__icontains=filter_data.get('salary_range', ''))
                                )
                                # Handle soft_skills filter separately
                                soft_skills_filter = filter_data.get('soft_skills', '')
                                if soft_skills_filter:
                                    job_posts = job_posts.filter(Q(soft_skills__icontains=f'"{soft_skills_filter}": True') |
                                                                Q(soft_skills__icontains=f"'{soft_skills_filter}': True"))
                            for job_post in job_posts:
                                job_post_serializer = JobPostSerializer(job_post)
                                if job_post_serializer.data:
                                    company_data = CompanyRegister.objects.get(user=job_post_serializer.data["user"])
                                    if company_data:
                                        updated_job_data = job_post_serializer.data.copy()
                                        try:
                                            updated_job_data["soft_skills"] = json.loads(updated_job_data["soft_skills"])
                                        except json.JSONDecodeError:
                                            updated_job_data["soft_skills"] = ast.literal_eval(updated_job_data["soft_skills"])
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
            print(f'Exception occurred in apply_job_post_filter_handler: {e}')
        return response_json
    
    def save_job_list_filter_handler(request, response_json):
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
                            # Apply similar filtering logic as in apply_job_post_filter_handler
                            filter_data = request.get("filterData", "")
                            search_value = request.get("search_value", "")
                            if search_value:
                                job_posts = job_posts.filter(
                                    Q(job_title__icontains=search_value) |
                                    Q(job_description__icontains=search_value) |
                                    Q(experience__icontains=search_value) |
                                    Q(salary_range__icontains=search_value) |
                                    Q(location__icontains=search_value) |
                                    Q(user__companyregister__company_name__icontains=search_value)
                                )
                            if filter_data:
                                job_posts = job_posts.filter(
                                    Q(job_title__icontains=filter_data.get('job_title', '')) &
                                    Q(location__icontains=filter_data.get('location', '')) &
                                    Q(salary_range__icontains=filter_data.get('salary_range', ''))
                                )
                                # Handle soft_skills filter separately
                                soft_skills_filter = filter_data.get('soft_skills', '')
                                if soft_skills_filter:
                                    job_posts = job_posts.filter(Q(soft_skills__icontains=f'"{soft_skills_filter}": True') |
                                                                Q(soft_skills__icontains=f"'{soft_skills_filter}': True"))
                            for job_post in job_posts:
                                job_post_serializer = JobPostSerializer(job_post)
                                if job_post_serializer.data:
                                    company_data = CompanyRegister.objects.get(user=job_post_serializer.data["user"])
                                    if company_data:
                                        updated_job_data = job_post_serializer.data.copy()
                                        try:
                                            updated_job_data["soft_skills"] = json.loads(updated_job_data["soft_skills"])
                                        except json.JSONDecodeError:
                                            updated_job_data["soft_skills"] = ast.literal_eval(updated_job_data["soft_skills"])
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
            print(f'Exception occurred in save_job_list_filter_handler: {e}')
        return response_json
    
    def exam_form_create_handler(request_data, response_json):
        try:
            exam_name = request_data.get("name", "")
            duration_minutes = request_data.get("duration_minutes", "")
            negative_marking_percentage = request_data.get("negative_marking_percentage", "")
            marksEach = request_data.get("marksEach", "")

            # Create a dictionary containing the data to be serialized
            data = {
                "exam_name": exam_name,
                "duration_minutes": duration_minutes if duration_minutes else 0,
                "negative_marking_percentage": negative_marking_percentage,
                "marksEach": marksEach,
            }
            # Create a new instance of the ExamFormSerializer with the data
            exam_form_serializer = ExamFormSerializer(data=data)

            # Check if the data is valid
            if exam_form_serializer.is_valid():
                # If valid, save the instance and set success message
                exam_form_serializer.save()
                response_json["message"] = "success"
            else:
                # If data is not valid, set an error message
                response_json["data"] = "Failed to create exam form"
        except Exception as e:
            # Handle other exceptions
            print(f'Exception occurred in exam_form_create_handler: {e}')
            response_json["data"] = "An error occurred while processing the request"
        
        return response_json


    def view_exam_forms(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                role = request.get("role", "")
                if login_db_data:
                    if login_db_data.role == role and role == 'employee':
                        exam_forms = ExamForm.objects.all()  
                        data = [{"exam_create_id":exam.exam_create_id, "exam_name": exam.exam_name, "duration_minutes": exam.duration_minutes} for exam in exam_forms]
                        if data:  
                            response_json["message"] = "success"  
                            response_json["data"] = data  
                        else:
                            response_json["message"] = "success"  
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong" 
        except Exception as e:
            print(f'Exception occurred while fetching exam forms: {e}')
        return response_json


    def exam_auth(request,response_json):
        try:
            try:
                exam_forms = ExamForm.objects.all()  

        # Serialize only exam name and duration
                data = [{"exam_name": exam.exam_name, "duration_minutes": exam.duration_minutes } for exam in exam_forms]

                if data:  # If there are serialized data
                    response_json["message"] = "success"  # Set success message
                    response_json["data"] = data  # Assign serialized data to response
                else:
                    response_json["message"] = "success"  # Set success message even if no data found

            except ObjectDoesNotExist:
                response_json["message"] = "success"
        except Exception as e:
            print(f'Exception occurred while fetching exam details: {e}')
            return response_json
            
    def exam_question_handler(request,response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get('username', ''), is_deleted=0)
                role = request.get("role", "")
                exam_create_id = request.get("exam_create_id", "")
                if login_db_data:
                    if login_db_data.role == role and role == 'employee':
                        if request:
                            for question_data in request.get("questions", []):
                                exam_db_data = ExamForm.objects.get(exam_create_id=exam_create_id)
                                if exam_db_data:
                                    question_data = {
                                        "exam_create_id": exam_create_id,
                                        "no_of_questions": 10,
                                        "question_desc": question_data.get('description') if question_data.get('description') else "NULL",
                                        "option_a":question_data['options'][0],
                                        "option_b":question_data['options'][1],
                                        "option_c":question_data['options'][2] if len(question_data['options']) > 2 else None,
                                        "option_d":question_data['options'][3] if len(question_data['options']) > 3 else None,
                                        "correct_ans":question_data['correctAnswer']
                                        }
                                    print(question_data)
                                    exam_question_serializer = ExamQuestionSerializer(data=question_data)
                                    if exam_question_serializer.is_valid():
                                        exam_question_serializer.save()
                                        response_json["message"] = "success"
                                    else:
                                        response_json["data"] = "Failed to add question" 
                                    print(exam_question_serializer.errors)
                                else:
                                    response_json["data"] = "Failed to retrieve exam data" 
                        else:
                            response_json["data"] = "Something went wrong" 
                    else:
                        response_json["data"] = "You are not authorized to view this page"
                else:
                    response_json["data"] = "You are not authorized to view this page"
            except ObjectDoesNotExist:
                response_json["message"] = "success"
        except Exception as e:
            print(f'Exception occurred while fetching exam details: {e}')
        return response_json