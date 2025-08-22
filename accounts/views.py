from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Assignment, Submission, Grade, User
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSerializer, RegistrationSerializer, LoginSerializer
from .permissions import IsTeacher, IsStudent
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role == 'teacher':
            serializer.save(updated_by=self.request.user)
        else:
            raise PermissionDenied("Only teachers are allowed to update assignments.")

class ListAssignmentView(ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Assignment.objects.filter(assigned_to = self.request.user)

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ListSubmissionView(ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Submission.objects.filter(assignment__created_by = self.request.user)

class GradeView(viewsets.ModelViewSet):
    queryset = Grade
    serializer_class = GradeSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class ListGradesView(ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Grade.objects.filter(graded_to = self.request.user)

class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_queryset().get(id=response.data['id'])  # get the created user
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response

class UserLogin(APIView):
    def post(self , request , format=None):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(username = email , password = password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            } , status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'Email or Password is incorrect'} , status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
#TODO patch and put

