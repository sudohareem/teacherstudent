from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Assignment, Submission, Grade, User
from .serializers import (
    AssignmentSerializer, SubmissionSerializer, GradeSerializer,
    RegistrationSerializer, LoginSerializer
)
from .permissions import IsTeacher, IsStudent


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsTeacher()]
        elif self.action in ["list_for_student"]:
            return [IsStudent()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role != "teacher":
            raise PermissionDenied("Only teachers can update assignments.")
        serializer.save(updated_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="list-for-student")
    def list_for_student(self, request):
        assignments = Assignment.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsStudent()]
        elif self.action in ["list_for_teacher"]:
            return [IsTeacher()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="list-for-teacher")
    def list_for_teacher(self, request):
        submissions = Submission.objects.filter(assignment__created_by=request.user)
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)


class GradeView(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsTeacher()]
        elif self.action in ["list_for_student"]:
            return [IsStudent()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="list-for-student")
    def list_for_student(self, request):
        grades = Grade.objects.filter(graded_to=request.user)
        serializer = self.get_serializer(grades, many=True)
        return Response(serializer.data)


class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = self.get_queryset().get(id=response.data['id'])
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response


class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
