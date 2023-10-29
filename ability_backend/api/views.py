from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from base.serializers import loginSerializer
from api.handlers.login_handler import LoginHandler

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
        response_json = handlers.get(request_data["type"])(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception Occcured in login api: {e}")
    return Response(response_json, status=401)
    
@api_view(['POST'])
def register_company_api(request):
    request_data = JSONParser().parse(request)
    data = {"username": request_data['companyUsername'], "password": request_data['companyPassword'], "is_deleted": 0}
    login_serializer=loginSerializer(data=data)
    if login_serializer.is_valid():
        login_serializer.save()
    return Response("Registered Successfully", status=200)