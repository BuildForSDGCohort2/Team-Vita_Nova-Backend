from abc import ABC

from rest_framework import serializers
import api.models as am
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_registration.api.serializers import DefaultRegisterUserSerializer


class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = am.AppUser
        exclude = ('password', 'user_permissions', 'groups',
                   'is_staff', 'is_superuser', 'last_login')

    def create(self, validated_data):
        appuser = am.AppUser.objects.create_user(**validated_data)
        return appuser


class UserEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = am.AppUser
        fields = ('email',)


class DefaultRegisterUserSerializerCustom(DefaultRegisterUserSerializer):

    class Meta:
        model = am.AppUser

    def create(self, validated_data, *args):
        appuser = am.AppUser.objects.create_user(**validated_data)
        appuser.save()
        return appuser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['id'] = user.id
        token['image'] = user.image

        return token


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = am.AppUser
        fields = ('image',)
