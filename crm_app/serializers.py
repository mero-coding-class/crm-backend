from rest_framework import serializers
from .models import User, Course, Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if user.role == User.Roles.SUPERADMIN:
                self.fields['role'].choices = [
                    (User.Roles.ADMIN, "Admin"),
                    (User.Roles.SALES_REP, "Sales Representative"),
                ]
            elif user.role == User.Roles.ADMIN:
                self.fields['role'].choices = [
                    (User.Roles.SALES_REP, "Sales Representative"),
                ]
            else:
                self.fields['role'].choices = []

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user