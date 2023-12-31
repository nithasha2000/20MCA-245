from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from api.handlers.login_handler import LoginHandler
from api.handlers.register_handler import RegisterHandler
from api.handlers.dashboard_handler import DashBoardHandler

@api_view(['GET'])
def index(request):
    return Response("Ability App")


@api_view(['POST'])
def login_api(request):
    response_json = {"message": "failed to fetch login", "data": ""}
    try:
        request_data = JSONParser().parse(request)
        if 'type' not in request_data:
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        if request_data['type'] == 'normal':
            if not all(key in request_data for key in ['username', 'password']):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        if request_data['type'] == 'google':
            if not all(key in request_data for key in ['access_token']):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        handlers = {
            "normal": LoginHandler.normal_login,
            "google": LoginHandler.google_login
        }
        response_json = handlers.get(request_data["type"])(request, request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception Occcured in login api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def logout_api(request):
    response_json = {"message": "failed to fetch logout", "data": ""}
    try:
        request_data = JSONParser().parse(request)
        response_json = LoginHandler.logout(request, request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception Occcured in logout api: {e}")
    return Response(response_json, status=401)
    
@api_view(['POST'])
def register_api(request):
    response_json = {"message": "failed to fetch register user", "data": ""}
    try:
        request_data = request.data
        if 'type' not in request_data:
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        if request_data['type'] == 'company_register':
            if not all(key in request_data for key in [
                'company_name', 'company_type', 'phone', 'email', 'profile',
                'website', 'license_no', 'confirm_companyPassword', 'company_password', 'business_license'
                ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        if request_data['type'] == "job_seeker_reg":
            if not all(key in request_data for key in [
                'type', 'firstName', 'lastName', 'dob', 
                'gender', 'phone', 'email', 'streetAddressLine1', 
                'streetAddressLine2', 'city', 'state', 'highestQualification', 
                'institution', 'cgpa', 'jobTitle', 'companyName', 
                'startDate', 'endDate', 'jobPassword',  'confirm_jobPassword', 
                'resume']):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        if request_data['type'] == "employee_register":
            if not all(key in request_data for key in [
                'type', 'firstName', 'lastName', 'email', 'confirm_employeePassword', 'employee_password']):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        handlers = {
            "company_register": RegisterHandler.company_register,
            "job_seeker_reg": RegisterHandler.job_seeker_register,
            "employee_register": RegisterHandler.employee_register,
        }
        response_json = handlers.get(request_data["type"])(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in registration api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def change_password_api(request):
    response_json = {"message": "failed to fetch change password", "data": ""}
    try:
        request_data = request.data
        if "type" in request_data and request_data.get("type") == "change-password":
            if not all(key in request_data for key in [
                    'username', 'role', 'newPassword', 'confirmPassword'
                    ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        else:
            if not all(key in request_data for key in [
                    'username', 'role', 'oldPassword', 'newPassword', 'confirmPassword'
                    ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        response_json = RegisterHandler.change_password(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in change password api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def forgot_password(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'email'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.forgot_password_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in forgot password api: {e}")
    return Response(response_json, status=401)
