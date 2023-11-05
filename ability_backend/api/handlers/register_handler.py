from base.models import Login
from base.serializers import loginSerializer, CompanyRegisterSerializer
from django.core.exceptions import ObjectDoesNotExist
from api.utilities.validation_utils import ValidateUtil
from api.utilities.common_utils import write_file


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
                        company_register_serializer.save()
                        login_serializer.save()
                        response_json["message"] = "success"
                        response_json["data"] = company_register_serializer.data
                    else:
                        response_json["message"] = "failed"
                        response_json["data"] = "Not able to add new user"
                else:
                    response_json["message"] = "failed"
                    response_json["data"] = "Not able to add new user"
        except Exception as e:
            print(f'Exception occured in company_register: {e}')
        return response_json