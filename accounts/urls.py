from django.contrib import admin
from django.urls import path, include
from .views import  AssignmentViewSet, SubmissionViewSet, GradeView, ListGradesView, ListAssignmentView, ListSubmissionView, UserRegister, UserLogin
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('assignmentapi', AssignmentViewSet, basename='assignmentapi')
router.register('submissionapi', SubmissionViewSet, basename='submissionapi')
router.register('gradeapi',GradeView , basename='grade' )

urlpatterns = [
    path('view-grade/',ListGradesView.as_view() , name='view-grade'),
    path('list-assingment/' , ListAssignmentView.as_view() , name = 'list-assignment' ),
    path('list-submission/' , ListSubmissionView.as_view() , name = 'list-submission' ),
    path('', include(router.urls)),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegister.as_view() , name='register'),
    path('login/',UserLogin.as_view() , name='login'),
    ]