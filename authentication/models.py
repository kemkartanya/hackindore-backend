from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from ckeditor.fields import RichTextField

from common.models import TimeStampedModelMixin, SoftDeletableModelMixin


class EmailNameChoices(models.TextChoices):
    WELCOME = "WELCOME", "Welcome"
    DRAWDOWN = "DRAWDOWN", "Drawdown"
    FORGOT_PASSWORD = "FORGOT_PASSWORD", "Forgot Password"
    LOGIN_DETAILS_PHASE1 = "LOGIN_DETAILS_PHASE1", "Login Details Phase 1"
    LOGIN_DETAILS_PHASE2 = "LOGIN_DETAILS_PHASE2", "Login Details Phase 2"
    LOGIN_DETAILS_PHASE3 = "LOGIN_DETAILS_PHASE3", "Login Details Phase 3"
    RULE_VIOLATION = "RULE_VIOLATION", "Rule Violation"
    PASSED_EVALUATION = "PASSED_EVALUATION", "Passed Evaluation"
    FAILED_REVIEW = "FAILED_REVIEW", "Failed Review"
    FAILED_KYC = "FAILED_KYC", "Failed KYC"
    PENDING_KYC = "PENDING_KYC", "Pending KYC"
    PASS_PHASE1_REVIEW = "PASS_PHASE1_REVIEW", "Pass Phase 1 Review"
    PENDING_PHASE1_REVIEW = "PENDING_PHASE1_REVIEW", "Pending Phase 1 Review"
    PENDING_PHASE2_REVIEW = "PENDING_PHASE2_REVIEW", "Pending Phase 2 Review"
    WITHDRAWAL_APPROVED = "WITHDRAWAL_APPROVED", "Withdrawal Approved"
    WITHDRAWAL_REJECTED = "WITHDRAWAL_REJECTED", "Withdrawal Rejected"
    WITHDRAWAL_REQUEST = "WITHDRAWAL_REQUEST", "Withdrawal Request"
    INACTIVITY_WARNING = "INACTIVITY_WARNING", "Inactivity Warning"
    COMPETITION_SIGNUP = "COMPETITION_SIGNUP", "Competition Signup"
    COMPETITION_LOGIN_DETAILS = "COMPETITION_LOGIN_DETAILS", "Competition Login Details"
    COMPETITION_ENDED = "COMPETITION_ENDED", "Competition Ended"
    COMPETITION_RUNNER_UP = "COMPETITION_RUNNER_UP", "Competition Runner Up"
    COMPETITION_STARTED = "COMPETITION_STARTED", "Competition Started"
    COMPETITION_WINNER = "COMPETITION_WINNER", "Competition Winner"


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(
    AbstractBaseUser, SoftDeletableModelMixin, PermissionsMixin, TimeStampedModelMixin
):
    mobile = models.CharField(max_length=20, unique=True, null=False, default="")
    email = models.EmailField(max_length=200, default="")
    full_name = models.CharField(max_length=100)
    picture = models.CharField(max_length=200, default="")
    email_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.mobile}"


class EmailTemplate(TimeStampedModelMixin):
    name = models.CharField(
        max_length=100,
        choices=EmailNameChoices.choices,
        default=EmailNameChoices.DRAWDOWN,
    )
    subject = models.CharField(max_length=200, default="")
    body = RichTextField(default="")

    def __str__(self):
        return self.name
