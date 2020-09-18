from rest_framework import serializers

from logic.models import Distributor, Sender


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = '__all__'


class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sender
        fields = '__all__'
