from base.models import Login
from base.serializers import loginSerializer
from django.core.exceptions import ObjectDoesNotExist
from google.oauth2 import id_token
from google.auth.transport import requests

class LoginHandler:
    def normal_login(request, request_data, response_json):
        try:
            request_username = request_data["username"]
            request_password = request_data["password"]
            login_db_data = Login.objects.get(username=request_username)
            if login_db_data.is_deleted:
                response_json["data"] = "Your is account deactivated contact admin"
                return response_json
            login_serializer = loginSerializer(login_db_data)
            if login_serializer.data:
                user_data = login_serializer.data
                password = user_data['password']
                if password == request_password:
                    response_json["message"] = "success"
                    response_json["data"] = login_serializer.data
                    response_json["data"].update({"type": "normal"})
                else:
                    response_json["message"] = "failed"
                    response_json["data"] = "Password Mismatch"
        except ObjectDoesNotExist:
            response_json["message"] = "failed"
            response_json["data"] = "Account doesnot exist"
        except Exception as e:
            print(f"Exception occured in normal_login handler: {e}")
        return response_json
    
    def google_login(request, request_data, response_json):
        try:
            access_token = request_data["access_token"]
            idinfo = id_token.verify_oauth2_token(access_token, requests.Request())
            if idinfo['aud'] not in ["873860161285-oinhstdgi1rg419l2afcv6na21c8an6o.apps.googleusercontent.com"]:
                response_json["message"] = "failed"
                response_json["data"] = "Google authentication failed"
            else:
                email = idinfo.get("email", '')
                login_db_data = Login.objects.get(username=email, is_deleted=0)
                login_serializer = loginSerializer(login_db_data)
                if login_serializer.data:
                    user_data = login_serializer.data
                    request.session['username'] = user_data['username']
                    request.session['role'] = user_data['role']
                    response_json["message"] = "success"
                    response_json["data"] = login_serializer.data
                    response_json["data"].update({"type": "google"})
                else:
                    response_json["message"] = "failed"
                    response_json["data"] = "Account doesnot exist"
        except ObjectDoesNotExist:
            response_json["message"] = "failed"
            response_json["data"] = "Account doesnot exist"
        except Exception as e:
            print(f"Exception occured in google_login handler: {e}")
        return response_json
    
    def logout(request, request_data, response_json):
        try:
            request_username = request_data["username"]
            request_role = request_data["role"]
            login_db_data = Login.objects.get(username=request_username, role=request_role, is_deleted=0)
            login_serializer = loginSerializer(login_db_data)
            if login_serializer.data:
                response_json["message"] = "success"
            else:
                response_json["message"] = "failed"
                response_json["data"] = "User is not logged in"
        except Exception as e:
            print(f"Exception occured in logout handler: {e}")
        return response_json