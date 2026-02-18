from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class Tbl_DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Tbl_Doctor
        fields='__all__'

class Tbl_PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Patient
        fields = '__all__'  

class Tbl_AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbl_Appointment
        fields = '__all__'


class DaySlotSerializer(serializers.Serializer):
    day = serializers.CharField(max_length=10)
    slots = serializers.ListField(
        child=serializers.CharField()
    )

class AvailableSlotSerializer(serializers.Serializer):
    available_slots = serializers.ListField(
        child=DaySlotSerializer()
    )


