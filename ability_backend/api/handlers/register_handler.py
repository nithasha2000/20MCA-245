import datetime
import smtplib
from base.models import Login
from base.serializers import loginSerializer, CompanyRegisterSerializer, JobSeekerRegisterSerializer
from django.core.exceptions import ObjectDoesNotExist
from api.utilities.validation_utils import ValidateUtil
from api.utilities.common_utils import write_file
from api.utilities import email_utils



class RegisterHandler:
    def company_register(request, response_json):
        try:
            try:
                valid, validate_resp = ValidateUtil.register_company_validate(request)
                if not valid:
                    response_json["data"] = validate_resp
                    return response_json
                register_data = {
                    "company_name": request.get("company_name", ''),
                    "company_type": request.get("company_type", ''),
                    "phone": int(request.get("phone", 0)),
                    "email": request.get("email", ''),
                    "profile": request.get("profile", ''),
                    "website": request.get("website", ''),
                    "license_no": int(request.get("license_no", 0)),
                }
                login_data = {
                    "username": register_data["email"],
                    "password": request.get("company_password", ''),
                    "role": "company",
                    "is_deleted": 0
                }
                Login.objects.get(username=login_data["username"])
                response_json["data"] = "Email already exist"
            except ObjectDoesNotExist:
                file_path = write_file(request.get('business_license'))
                if not file_path:
                    response_json["data"] = "Failed to save license file"
                    return response_json
                register_data.update({"business_license": file_path})
                company_register_serializer=CompanyRegisterSerializer(data=register_data)
                if company_register_serializer.is_valid():
                    login_serializer=loginSerializer(data=login_data)
                    if login_serializer.is_valid():
                        email_body = f"Welcome {register_data['company_name']} to Ability portal"
                        sub=f"User registration mail"
                        email_html_path = r"D:\20MCA-245\ability-project\20MCA-245\ability_backend\api\utilities\link_email.html"
                        confirmation_message = f"New user has registered to Ability Portal!!<br> User Name : {register_data['company_name']}.<br> Login to view details."
                        subject = f"User registration confirmation mail"
                        if email_utils.welcome_sender(login_data["username"],sub,email_body, email_html_path):
                           email_utils.welcome_sender("abilityportal@gmail.com",subject,confirmation_message,email_html_path)
                           company_register_serializer.save()
                           login_serializer.save()
                           response_json["message"] = "success"
                           response_json["data"] = company_register_serializer.data 
                           print("User registered")
                    else:
                        response_json["data"] = "Not able to add new user"
                else:
                    response_json["data"] = "Not able to add new user"
        except Exception as e:
            print(f'Exception occured in company_register: {e}')
        return response_json
    
    def job_seeker_register(request, response_json):
        try:
            try:
                valid, validate_resp = ValidateUtil.job_seeker_reg_validate(request)
                if not valid:
                    response_json["data"] = validate_resp
                    return response_json
                start_date = request.get("startDate", '')
                end_date = request.get("endDate", '')
                register_data = {
                    'first_name': request.get("firstName", ''), 
                    'last_name': request.get("lastName", ''),
                    'dob': datetime.datetime.strptime(request.get("dob", ''), "%Y-%m-%d").date(),
                    'gender': request.get("gender", ''), 
                    'phone': int(request.get("phone", 0)),
                    'email': request.get("email", ''),
                    'street_address_line1': request.get("streetAddressLine1", ''),
                    'street_address_line2': request.get("streetAddressLine2", ''),
                    'city': request.get("city", ''),
                    'state': request.get("state", ''),
                    'highest_qualification': request.get("highestQualification", ''),
                    'institution': request.get("institution", ''),
                    'cgpa': float(request.get("cgpa", 0)),
                    'resume': request.get("resume", ''),
                    'experience_type': request.get("experienceType", ''),
                    'job_title': request.get("jobTitle", ''), 
                    'company_name': request.get("companyName", ''),
                    'start_date': datetime.datetime.strptime(start_date, "%Y-%m-%d").date() if start_date != 'undefined' else None,
                    'end_date': datetime.datetime.strptime(end_date, "%Y-%m-%d").date() if end_date != 'undefined' else None

                }
                login_data = {
                    "username": register_data["email"],
                    "password": request.get("jobPassword", ''),
                    "role": "job_seeker",
                    "is_deleted": 0
                }
                Login.objects.get(username=login_data["username"])
                response_json["data"] = "Email already exist"
            except ObjectDoesNotExist:
                file_path = write_file(request.get('resume'))
                if not file_path:
                    response_json["data"] = "Failed to save resume"
                    return response_json
                register_data.update({"resume": file_path})
                print(register_data)
                job_seeker_reg__serializer=JobSeekerRegisterSerializer(data=register_data)
                if job_seeker_reg__serializer.is_valid():
                    login_serializer=loginSerializer(data=login_data)
                    if login_serializer.is_valid():
                        email_body = f"Welcome {register_data['first_name']} to Ability portal"
                        sub=f"User registration mail"
                        email_html_path = r"D:\20MCA-245\ability-project\20MCA-245\ability_backend\api\utilities\link_email.html"
                        confirmation_message = f"New user has registered to Ability Portal!! <br>User Name : {register_data['first_name']}. <br>Login to view details."
                        subject = f"User registration confirmation mail"
                        if email_utils.welcome_sender(login_data["username"],sub, email_body, email_html_path):
                           email_utils.welcome_sender("abilityportal@gmail.com",subject,confirmation_message,email_html_path)
                           job_seeker_reg__serializer.save()
                           login_serializer.save()
                           response_json["message"] = "success"
                           response_json["data"] = job_seeker_reg__serializer.data
                    else:
                        response_json["data"] = "Not able to add new user"
                else:
                    response_json["data"] = "Not able to add new user"
        except Exception as e:
            print(f'Exception occured in job_seeker_register: {e}')
        return response_json
    
    def change_password(request, response_json):
        try:
            try:
                login_db_data = Login.objects.get(username=request.get("username", ''), role=request.get("role", ''))
                login_serializer = loginSerializer(login_db_data)
                if login_serializer.data:
                    user_data = login_serializer.data
                    password = user_data['password']
                    if password == request.get("oldPassword", ''):
                        valid, validate_resp = ValidateUtil.change_password_valid(request)
                        if not valid:
                            response_json["data"] = validate_resp
                            return response_json
                        if request.get("oldPassword", '') != request.get("newPassword"):
                            login_db_data.password = request.get("newPassword")
                            login_db_data.save()
                            login_serializer = loginSerializer(login_db_data)
                            response_json["message"] = "success"
                            response_json["data"] = "Password changed"
                        else:
                            response_json["data"] = "New Password cannot be the same as current password"
                    else:
                        response_json["data"] = "Enter your current account password"
                else:
                    response_json["data"] = "Account doesnot exist"
            except ObjectDoesNotExist:
                response_json["data"] = "Something went wrong"
        except Exception as e:
            print(f'Exception occured in change password: {e}')
        return response_json
    