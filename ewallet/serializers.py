from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_registration.api.serializers import DefaultRegisterUserSerializer

import ewallet.models as wa

class EwalletAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = wa.Accounts
        fields = "__all__"

    def create(self, validated_data):
        account = wa.AppUser.objects.create_account(**validated_data)
        return account
