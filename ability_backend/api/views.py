from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from api.handlers.login_handler import LoginHandler
from api.handlers.register_handler import RegisterHandler

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
                'website', 'license_no','business_license', 'confirm_companyPassword', 'company_password'
                ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        handlers = {
            "company_register": RegisterHandler.company_register
        }
        response_json = handlers.get(request_data["type"])(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
        return Response("Registered Successfully", status=200)
    except Exception as e:
        print(f"Exception occured in registration api: {e}")
    return Response(response_json, status=401)