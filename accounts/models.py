from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, role, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, role="teacher", password=None):
        user = self.create_user(
            email=email,
            name=name,
            role=role,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "role"]

    def __str__(self):
        return f"{self.name} ({self.email})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignments_created"
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignments_received"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.OneToOneField(
        Assignment, on_delete=models.CASCADE, related_name="submission"
    )
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="submissions"
    )
    solution_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.assignment.title}"



class Grade(models.Model):
    assignment = models.OneToOneField(
        Assignment, on_delete=models.CASCADE, related_name="grade"
    )
    graded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="grades_given"
    )
    graded_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="grades_received"
    )
    score = models.IntegerField()
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.score} - {self.assignment.title}"
