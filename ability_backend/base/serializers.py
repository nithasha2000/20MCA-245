from rest_framework import serializers
from base.models import Login, CompanyRegister, JobSeekerRegister, UserNotifications

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

class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotifications
        fields = '__all__'