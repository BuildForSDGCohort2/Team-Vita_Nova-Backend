from cloudinary import uploader
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import AppUser
from logic.models import Sender, Distributor
from logic.serializers import SenderSerializer, DistributorSerializer


# Create your views here.


class DistributorViewSet(viewsets.ViewSet):

    # Distributor

    @action(detail=False, permission_classes=[IsAuthenticated])
    def get_distributors(self, request):

        try:
            queryset = []
            distributor_ids = []
            send_orders = Sender.objects.filter(status='Open')
            for send_order in send_orders:
                distributors = Distributor.objects.filter(departure=send_order.departure,
                                                          destination=send_order.destination,
                                                          active_distributor=True,
                                                          travel_schedule__range=[send_order.created,
                                                                                  send_order.travel_schedule])
                for distributor in distributors:
                    if len(distributor_ids) == 0:
                        queryset.append(distributor)
                        distributor_ids.append(distributor.id)
                    elif not distributor_ids.__contains__(distributor.id):
                        queryset.append(distributor)
                        distributor_ids.append(distributor.id)

            serializer = DistributorSerializer(queryset, many=True)
            if len(serializer.data) == 0:
                data = {'message': 'User does not have any distributor yet'}
            else:
                data = serializer.data
        except AppUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Distributor.DoesNotExist:
            return Response({'message': 'User does not have any distributor yet'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def post_distributor_request(self, request):
        serializer = DistributorSerializer(data=request.data)
        if serializer.is_valid():
            user = AppUser.objects.get(email=request.user.email)
            serializer.save(user=user)
            data = {"message": "Distributor request added successfully"}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {"message": "An error occurred, check the fields for omission or duplicates"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class SenderViewSet(viewsets.ViewSet):

    # Sender

    @action(detail=False, permission_classes=[IsAuthenticated])
    def get_open_send_orders(self, request):

        try:
            user = request.user
            if 'action' in request.data:
                queryset = Sender.objects.filter(booked_distributor=user, status='Open')
                serializer = SenderSerializer(queryset, many=True)
                if len(serializer.data) == 0:
                    data = {'message': 'Distributor does not have any booked order yet'}
                else:
                    data = serializer.data
            else:
                queryset = Sender.objects.filter(user=user, status='Open')
                serializer = SenderSerializer(queryset, many=True)
                if len(serializer.data) == 0:
                    data = {'message': 'User does not have any send order yet'}
                else:
                    data = serializer.data
        except AppUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Sender.DoesNotExist:
            return Response({'message': 'Send order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def post_send_order(self, request, *args, **kwargs):

        try:
            serializer = SenderSerializer(data=request.data)
            user = AppUser.objects.get(email=request.user.email)
            if 'goods_image' not in request.data:
                if serializer.is_valid():
                    serializer.save(user=user)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                image_url = request.data['goods_image']
                if serializer.is_valid():
                    image = uploader.upload(image_url)
                    serializer.save(user=user, goods_image=image['url'])
                    print(image['url'])
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AppUser.DoesNotExist:
            response = {"message": "user does not exist"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Send order added successfully"}, status=status.HTTP_201_CREATED)
