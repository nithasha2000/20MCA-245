from rest_framework import serializers
from base.models import Login, CompanyRegister

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'
        
class CompanyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRegister
        fields = '__all__'
        