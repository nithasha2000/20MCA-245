from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from api.handlers.login_handler import LoginHandler
from api.handlers.register_handler import RegisterHandler
from api.handlers.dashboard_handler import DashBoardHandler

@api_view(['POST'])
def view_users(request):
    response_json = {"message": "failed to fetch users", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'username', 'role'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.view_users(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in view users api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def account_activation(request):
    response_json = {"message": "failed to change activation state", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'username', 'role', 'change_username'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.account_activation_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in activation of accounts api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def dashboard_sidebar(request):
    response_json = {"message": "failed to load side bar", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'email', 'role'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.dashboard_sidebar_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in activation of accounts api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def verify_otp(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'email', 'otp'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.verify_otp_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in verify otp api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def view_notifications(request):
    response_json = {"message": "failed to fetch notifications", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'username', 'role'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.view_notifications(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in view notifications api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def job_post(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if "type" not in request_data:
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        if "type" in request_data and request_data.get("type") == "create":
            if not all(key in request_data for key in [
                    'user_data', 'job_title', 'job_description', 'experience', 'location', 'salary_range', 'application_deadline'
                    ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        if "type" in request_data and request_data.get("type") == "edit":
            if not all(key in request_data for key in [
                    'job_post_id', 'user_data', 'job_title', 'job_description', 'experience', 'location', 'salary_range', 'application_deadline'
                    ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        if "type" in request_data and request_data.get("type") == "delete":
            if not all(key in request_data for key in [
                    'username', 'role','job_post_id'
                    ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        handlers = {
            "create": DashBoardHandler.job_post_create_handler,
            "edit": DashBoardHandler.job_post_edit_handler,
            "delete": DashBoardHandler.job_post_delete_handler
        }
        response_json = handlers.get(request_data["type"])(request, request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in job_post api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def view_job_list(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.view_job_list_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in view_job_list api: {e}")
    return Response(response_json, status=401)
