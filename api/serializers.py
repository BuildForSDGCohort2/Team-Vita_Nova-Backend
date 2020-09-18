from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_registration.api.serializers import DefaultRegisterUserSerializer

import api.models as am


class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = am.AppUser
        exclude = ('password', 'user_permissions', 'groups',
                   'is_staff', 'is_superuser', 'last_login')

    def create(self, validated_data):
        app_user = am.AppUser.objects.create_user(**validated_data)
        return app_user


class UserEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = am.AppUser
        fields = ('email',)


class DefaultRegisterUserSerializerCustom(DefaultRegisterUserSerializer):

    class Meta:
        model = am.AppUser

    def create(self, validated_data, *args):
        app_user = am.AppUser.objects.create_user(**validated_data)
        app_user.save()
        return app_user


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


class UserReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = am.UserReview
        fields = '__all__'
