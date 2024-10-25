from rest_framework import serializers
# from .models import (ExamDetails,ExamMode,ExamSlot,
#                      PaperType,Region,State,City,
#                      ExamCenter,ExamDevice,ExamRole,
                    #  )
from .models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

no_special_character = RegexValidator(
                        regex=r'^[a-zA-Z0-9-]+$',
                        message="Special charaters not allowed"
)


def no_special_character_fun(field_name):
    def validator(value):
        if not re.search(r'^[a-zA-Z0-9-]+$', value):
            raise ValidationError(f"No special characters allowed for {field_name}")
        return value
    return validator

class ExamDetailSerializer(serializers.ModelSerializer):
    examname = serializers.CharField(validators=[no_special_character_fun('examname')])
    # examname = serializers.CharField(validators=[RegexValidator(regex=r'^[a-zA-Z0-9-]+$',message="Special charaters for examname not allowed")])
    clientname = serializers.CharField(validators=[no_special_character])
    exam_hash = serializers.CharField(validators=[no_special_character])
    examcode = serializers.CharField(validators=[no_special_character])
    class Meta:
        model = ExamDetails
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExamModeSerializer(serializers.ModelSerializer):
    exammode = serializers.CharField(validators=[no_special_character])
    class Meta:
        model = ExamMode
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExamSlotSerializer(serializers.ModelSerializer):
    examslot = serializers.CharField(validators=[no_special_character])
    class Meta:
        model = ExamSlot
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PaperTypeSerializer(serializers.ModelSerializer):
    papertype = serializers.CharField(validators=[no_special_character])
    class Meta:
        model = PaperType
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class RegionSerializer(serializers.ModelSerializer):
        regionname = serializers.CharField(validators=[no_special_character])
        examcode = serializers.StringRelatedField()
        class Meta:
            model = Region
            fields = '__all__'
            read_only_fields = ['id', 'created_at', 'updated_at']

class StateSerializer(serializers.ModelSerializer):
        statename = serializers.CharField(validators=[no_special_character])
        class Meta:
            model = State
            fields = '__all__'
            read_only_fields = ['id', 'created_at', 'updated_at']

class CitySerializer(serializers.ModelSerializer):
        cityname = serializers.CharField(validators=[no_special_character])
        class Meta:
            model = City
            fields = '__all__'
            read_only_fields = ['id', 'created_at', 'updated_at']
            
class ExamCenterSerializer(serializers.ModelSerializer):
        class Meta:
            model = ExamCenter
            fields = '__all__'
            read_only_fields = ['id', 'created_at', 'updated_at']

class ExamDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamDevice
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExamRoleSerializer(serializers.ModelSerializer):
     class Meta:
        model = ExamRole
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExamMemberserializer(serializers.ModelSerializer):
     class Meta:
        model = ExamMember
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']