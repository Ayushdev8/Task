from accounts.models import UserModel
from .models import AddTask 
from rest_framework import serializers
from utils import send_confirmation_email

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'phone_no',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        if not data.get('phone_no'):
            raise serializers.ValidationError("Phone number is required")
        return data
        
    def create(self, validated_data):
        validated_data.pop('password2')

        user = UserModel.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_no=validated_data.get('phone_no'),

        )
        user.save()
        send_confirmation_email(user)
        
        return user
    
class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTask
        fields = '__all__'
        read_only_fields = ['user']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class TotalTaskSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    progress_tasks = serializers.IntegerField()