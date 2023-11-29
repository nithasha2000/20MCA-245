from django.db import models

class Login(models.Model):  # Model class names are typically capitalized.
    user_id = models.CharField(primary_key=True, max_length=255)  # Use AutoField for primary keys.
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
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
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
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    street_address_line1 = models.CharField(max_length=255) 
    street_address_line2 = models.CharField(max_length=255) 
    city = models.CharField(max_length=255) 
    state = models.CharField(max_length=255) 
    highest_qualification = models.CharField(max_length=255) 
    institution = models.CharField(max_length=255) 
    cgpa = models.FloatField(default=0.0)
    resume = models.CharField(max_length=255) 
    experience_type = models.CharField(max_length=255, default="fresher")
    job_title = models.CharField(max_length=255, null=True) 
    company_name = models.CharField(max_length=255, null=True) 
    start_date = models.DateField(default=None, null=True)
    end_date = models.DateField(default=None, null=True)

    class Meta:
        app_label = 'base'

class JobPost(models.Model):  # Model class names are typically capitalized.
    job_post_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=255)
    job_description = models.CharField(max_length=255) 
    experience = models.CharField(max_length=255) 
    location = models.CharField(max_length=255) 
    salary_range = models.CharField(max_length=255) 
    application_deadline = models.DateField(default=None)
    post_status = models.CharField(max_length=255) 
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    class Meta:
        app_label = 'base'
        
class JobApplications(models.Model):  # Model class names are typically capitalized.
    job_applications_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    application_status = models.CharField(max_length=255) 
    class Meta:
        app_label = 'base'
        
class SaveJobPosts(models.Model):  # Model class names are typically capitalized.
    save_job_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    class Meta:
        app_label = 'base'

class UserNotifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Login, on_delete=models.CASCADE)
    notification = models.CharField(max_length=255)
    viewed = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'base'