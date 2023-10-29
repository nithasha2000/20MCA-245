from rest_framework import serializers
from base.models import Login

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'