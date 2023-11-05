import re
from api.utilities.common_utils import validation_dict


class ValidateUtil:
    def register_company_validate(request):
        errors = []
        valid = True
        try:
            if 'company_name' in request:
                if not re.match(validation_dict.get("name", r'^[a-zA-Z0-9\s\-_]+$'), request["company_name"]):
                    errors.append("For Company Name only letters, numbers, spaces, and certain special characters like hyphens and underscores")
                    valid = False
            if 'company_type' in request:
                if not re.match(validation_dict.get("name", r'^[a-zA-Z0-9\s\-_]+$'), request["company_type"]):
                    errors.append("For Company Type only letters, numbers, spaces, and certain special characters like hyphens and underscores")
                    valid = False
            if 'phone' in request:
                if not re.match(validation_dict.get("phone", r'^\d{10}$'), request["phone"]):
                    errors.append("10 digit phone number is required")
                    valid = False
            if 'email' in request:
                if not re.match(validation_dict.get("email", r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'), request["email"]):
                    errors.append("Valid email id is required")
                    valid = False
            if 'profile' in request:
                if not re.match(validation_dict.get("name", r'^[a-zA-Z0-9\s\-_]+$'), request["company_name"]):
                    errors.append("For profile only letters, numbers, spaces, and certain special characters like hyphens and underscores")
                    valid = False
            if 'license_no' in request:
                if not re.match(validation_dict.get("phone", r'^\d{10}$'), request["license_no"]):
                    errors.append("10 digit license no is required")
                    valid = False
            if 'company_password' in request:
                if not re.match(validation_dict.get("password", ''), request["company_password"]):
                    errors.append("Password should be at least 8 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character.")
                    valid = False
            if 'confirm_companyPassword' in request:
                if not re.match(validation_dict.get("password", ''), request["confirm_companyPassword"]):
                    errors.append("Confirm Password should be at least 8 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character.")
                    valid = False
            if 'confirm_companyPassword' in request and 'company_password' in request:
                if request.get("company_password") != request.get("confirm_companyPassword"):
                    errors.append("Password mismatch ! Both password and confirm password should be same")
                    valid = False
        except Exception as e:
            print(f"Exception occured in company validation: {e}")
            valid =False
        return valid, errors