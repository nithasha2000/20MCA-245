from django.http import HttpResponse
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
    response_json = {"message": "failed to fetch notifications", "data": "", "count": 0}
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
def mark_notifications(request):
    response_json = {"message": "failed to mark notifications", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'username', 'role', "notification_id"
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.mark_notifications_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in mark_notifications api: {e}")
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
                    'user_data', 'job_title', 'job_description', 'experience', 'location', 'soft_skills', 'salary_range', 'application_deadline'
                    ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        if "type" in request_data and request_data.get("type") == "edit":
            if not all(key in request_data for key in [
                    'job_post_id', 'user_data', 'job_title', 'job_description', 'experience', 'location', 'soft_skills', 'salary_range', 'application_deadline'
                    ]):
                response_json["data"] = "Unprocessible entity"
                return Response(response_json, status=422)
        if "type" in request_data and request_data.get("type") == "close":
            if not all(key in request_data for key in [
                    'username', 'role','job_post_id'
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
            "status": DashBoardHandler.job_post_status_handler,
            "delete": DashBoardHandler.job_post_delete_handler,
        }
        response_json = handlers.get(request_data["type"])(request, request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in job_post api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def view_job_list(request):
    response_json = {"message": "failed", "data": []}
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

@api_view(['POST'])
def job_post_filter(request):
    response_json = {"message": "failed", "data": []}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role', 'search_value', 'filterData'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.job_post_filter_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in job_post_filter api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def job_post_approve(request):
    response_json = {"message": "failed", "data": []}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'type', 'status', 'username', 'role', 'job_post_id'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.job_post_approve_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in job_post_approve api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def apply_job(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role', 'job_post_id'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.apply_job_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in apply_job api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def unapply_job(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role', 'applied_post'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.unapply_job_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in unapply_job api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def save_job_post(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role', 'job_post_id'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.save_job_post_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in save_job_post api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def applied_job_list(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.applied_job_list_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in applied_job_list api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def view_save_job_post(request):
    response_json = {"message": "failed", "data": []}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.view_save_job_post_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in view_save_job_post api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def unsave_job(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role', 'save_post'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.unsave_job_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in unsave_job api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def view_applicants(request):
    response_json = {"message": "failed to fetch applicants", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'username', 'role', 'job_post_id'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.view_applicants_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in view_applicants api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def download_applicant_resume(request):
    response_json = {"message": "failed to fetch applicants", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'username', 'role', 'job_seeker_id'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.download_applicant_resume_handler(request_data, response_json)
        if response_json["message"] == "success":
            return HttpResponse(response_json["data"], status=200, content_type='application/pdf')
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in download_applicant_resume api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def shortlist_candidate(request):
    response_json = {"message": "failed to fetch applicants", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
                'username', 'role', 'job_seeker_id', 'job_id'
                ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.shortlist_candidate_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in shortlist_candidate api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def apply_job_post_filter(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role', 'search_value', 'filterData'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.apply_job_post_filter_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in apply_job_post_filter api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def save_job_list_filter(request):
    response_json = {"message": "failed", "data": ""}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role', 'search_value', 'filterData'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.save_job_list_filter_handler(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f"Exception occured in save_job_list_filter api: {e}")
    return Response(response_json, status=401)

@api_view(['POST'])
def view_exam_forms(request):
    response_json = {"message": "failed", "data": []}
    try:
        request_data = request.data
        if not all(key in request_data for key in [
            'username', 'role'
            ]):
            response_json["data"] = "Unprocessible entity"
            return Response(response_json, status=422)
        response_json = DashBoardHandler.view_exam_forms(request_data, response_json)
        if response_json:
            return Response(response_json, status=200)
    except Exception as e:
        print(f'Exception occurred while fetching exam forms: {e}')
    return Response(response_json, status=401)  # Return the response JSON object with status code 200
