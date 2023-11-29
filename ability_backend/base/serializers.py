from rest_framework import serializers
from base.models import (
    JobApplications,
    Login, 
    CompanyRegister, 
    JobSeekerRegister,
    SaveJobPosts, 
    UserNotifications,
    JobPost
)

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRegister
        fields = '__all__'

class JobSeekerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerRegister
        fields = '__all__'
        
class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'
        
class JobApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplications
        fields = '__all__'
        
class SaveJobPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveJobPosts
        fields = '__all__'


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotifications
        fields = '__all__'