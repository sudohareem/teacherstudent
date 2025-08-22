from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Assignment, Submission, Grade

class UserAdmin(BaseUserAdmin):
    list_display = ["email", "name", "password", "role", "is_admin"]
    list_filter = ["email"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_admin", "role"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password", "role"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(User, UserAdmin)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description','assigned_to']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'assignment', 'graded_to', 'score']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'assignment', 'solution_text', 'submitted_at']






