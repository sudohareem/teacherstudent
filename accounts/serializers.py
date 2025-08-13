from rest_framework import serializers
from .models import User, Assignment, Submission, Grade


# User Serializer with password hashing
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'password', 'is_active', 'is_admin', 'created_at']
        read_only_fields = ['id', 'is_active', 'is_admin', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class AssignmentSerializer(serializers.ModelSerializer):
    #created_by = serializers.StringRelatedField(read_only=True)
    #assigned_to = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'assigned_to', ]


class SubmissionSerializer(serializers.ModelSerializer):
    #assignment = serializers.StringRelatedField(read_only=True)
    #submitted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'solution_text', 'submitted_at']


class GradeSerializer(serializers.ModelSerializer):
   # assignment = serializers.StringRelatedField(read_only=True)
    #graded_by = serializers.StringRelatedField(read_only=True)
    #graded_to = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'assignment', 'graded_to', 'score']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'name' , 'email' ,'password' , 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email' ,'password']