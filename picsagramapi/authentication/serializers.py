import djoser
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from djoser.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from .constants import CustomMessages


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
class CustomTokenCreateSerializer(TokenObtainSerializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})

    default_error_messages = {
        "inactive_account": CustomMessages.INACTIVE_ACCOUNT_ERROR,
        "invalid_email" : CustomMessages.EMAIL_NOT_FOUND,
        "invalid_password": CustomMessages.INVALID_PASSWORD_ERROR,
    }

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields[settings.LOGIN_FIELD] = serializers.CharField(required=False)

    def validate(self, attrs):
        password = attrs.get("password")
        params = {djoser.conf.settings.LOGIN_FIELD: attrs.get(djoser.conf.settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )

        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_password")
            if not self.user:
                self.fail("invalid_email")
        if self.user and self.user.is_active:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)

            return data

        if self.user and not self.user.is_active:
            self.fail("inactive_account")
        self.fail("invalid_credentials")
