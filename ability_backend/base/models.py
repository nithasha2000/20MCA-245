from django.db import models

class Login(models.Model):  # Model class names are typically capitalized.
    id = models.AutoField(primary_key=True)  # Use AutoField for primary keys.
    username = models.CharField(max_length=255)  # Use CharField for text fields.
    password = models.CharField(max_length=255)  # Use CharField for text fields.
    role = models.CharField(max_length=255)
    is_deleted = models.IntegerField(default=0)  # Use IntegerField for integers.

    class Meta:
        app_label = 'base'

class CompanyRegister(models.Model):  # Model class names are typically capitalized.
    company_id = models.AutoField(primary_key=True)  # Use AutoField for primary keys.
    company_name = models.CharField(max_length=255)  # Use CharField for text fields.
    company_type = models.CharField(max_length=255)  # Use CharField for text fields.
    phone = models.PositiveBigIntegerField(default=0)
    email = models.CharField(max_length=255)  # Use IntegerField for integers.
    profile = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    license_no = models.PositiveBigIntegerField(default=0)
    business_license = models.CharField(max_length=255)

    class Meta:
        app_label = 'base'
        
class JobSeekerRegister(models.Model):  # Model class names are typically capitalized.
    job_seeker_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255) 
    dob = models.DateField() 
    gender = models.CharField(max_length=255) 
    phone = models.PositiveBigIntegerField(default=0)
    email = models.CharField(max_length=255) 
    street_address_line1 = models.CharField(max_length=255) 
    street_address_line2 = models.CharField(max_length=255) 
    city = models.CharField(max_length=255) 
    state = models.CharField(max_length=255) 
    highest_qualification = models.CharField(max_length=255) 
    institution = models.CharField(max_length=255) 
    cgpa = models.PositiveBigIntegerField(default=0)
    resume = models.CharField(max_length=255) 
    job_title = models.CharField(max_length=255) 
    company_name = models.CharField(max_length=255) 
    start_date= models.DateField() 
    end_date = models.DateField() 

    class Meta:
        app_label = 'base'
        