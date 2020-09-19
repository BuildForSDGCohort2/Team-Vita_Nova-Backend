from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import AppUser

import ewallet.models as ew
import ewallet.serializers as ews

class EwalletViewSets(viewsets.ViewSet):

    @action(detail=False, permission_classes=[IsAuthenticated])
    def view_transactions(self, request):
        try:
            queryset = ew.Accounts.objects.get(user = request.user.id)
            serializer = ews.EwalletAccountSerializer(queryset)
        except AppUser.DoesNotExist:
            return Response({'message':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data,status=status.HTTP_200_OK)


    @action(detail=False, permission_classes=[IsAuthenticated])
    def view_balance(self, request):
        try:
            queryset = ew.Accounts.objects.filter(user = request.user.id).latest('user')
            serializer = ews.EwalletAccountSerializer(queryset)
        except AppUser.DoesNotExist:
            return Response({'message':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data,status=status.HTTP_200_OK)