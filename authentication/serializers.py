from rest_framework import serializers
from django.conf import settings
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from authentication.models import User
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.serializers import (
    PasswordResetConfirmSerializer as _PasswordResetConfirmSerializer,
)
from django.utils.encoding import force_str
from rest_framework.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm as ResetPasswordForm


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "mobile",
            "full_name",
        ]
        read_only_fields = [
            "id",
            "mobile",
        ]


class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email=email.lower()).exists():
            raise serializers.ValidationError("Email address already in use")
        return email.lower()

    def custom_signup(self, request, user):
        user.full_name = self.validated_data.get("full_name", "")
        user.save(update_fields=["full_name"])


class CustomPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = ResetPasswordForm

    def get_email_options(self):
        return {
            "subject_template_name": "email/password_reset_subject.txt",
            "email_template_name": "email/password_reset_email.html",
            "extra_email_context": {
                "domain": settings.FRONTEND_URL.replace("http://", "").replace(
                    "https://", ""
                )
            },
        }


class PasswordResetConfirmSerializer(_PasswordResetConfirmSerializer):

    def validate(self, attrs):
        from allauth.account.forms import default_token_generator

        try:
            uid = force_str(attrs["uid"])
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({"uid": [_("Invalid value")]})

        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise ValidationError({"token": [_("Invalid value")]})

        self.custom_validation(attrs)

        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs
