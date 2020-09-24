import cloudinary.uploader
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

import api.models as am
import api.permissions as ap
import api.serializers as aps

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from django.db.models import Count

import json


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = aps.CustomTokenObtainPairSerializer


class UserViewSets(viewsets.ModelViewSet):

    """
    The user search endpoint searches based on
    email or username
    /api/user/filter_user//?s=<value?
    """

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    queryset = am.AppUser.objects.all()
    serializer_class = aps.AppUserSerializer

    @action(detail=False, methods=['put'])
    def upload_profile_image(self, request):

        """
        image should be passed as a base64 string
        the the body of the request
        """

        try:
            user = am.AppUser.objects.get(username=request.user.username)
            serializer = aps.UserImageSerializer(data=request.data)
            if serializer.is_valid():
                data = request.data['image']
                image = cloudinary.uploader.upload(data)
                user.image = image['url']
                user.save()
                url = image['url']
                return Response({'image_string': url}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({'status': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ViewSet):

    @action(detail=False, permission_classes=[IsAuthenticated])
    def get_profile(self, request):

        try:
            if 'email' not in request.data:
                email = request.user.email
            else:
                email = request.data['email']
            queryset = am.AppUser.objects.get(email=email)
            serializer = aps.AppUserSerializer(queryset)
        except am.AppUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], permission_classes=[ap.IsOwner, IsAuthenticated])
    def update_profile(self, request):

        user = am.AppUser.objects.get(email=request.user.email)
        serializer = aps.AppUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {"message": "User information updated successfully"}
        else:
            data = {"message": "An error occurred, check the fields for omission or id duplicate"}
        return Response(data, status=status.HTTP_200_OK)


class UserReviewViewSet(viewsets.ViewSet):

    """
    User Review
    """

    @action(detail=False, permission_classes=[IsAuthenticated])
    def get_user_review(self, request):

        try:
            if 'user' in request.data:
                email = request.data['user']
            else:
                email = request.user.email
            user = am.AppUser.objects.get(email=email)
            queryset = am.UserReview.objects.filter(user=user)
            serializer = aps.UserReviewSerializer(queryset, many=True)
            if len(serializer.data) == 0:
                data = {'message': 'User does not have any review yet'}
            else:
                data = serializer.data
        except am.AppUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except am.UserReview.DoesNotExist:
            return Response({'message': 'User does not have any review yet'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def post_user_review(self, request, *args, **kwargs):

        serializer = aps.UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            user = am.AppUser.objects.get(id=request.data.get('user'))
            reviewer = am.AppUser.objects.get(email=request.user.email)
            if reviewer == user:
                data = {"message": "Sorry, you can't review yourself"}
                return Response(data=data, status=status.HTTP_403_FORBIDDEN)
            else:
                serializer.save(reviewer=reviewer)
                data = {"message": "Review added successfully"}
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {"message": "An error occurred, check the fields for omission or duplicates"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

def check_user_with_token(request):
    user_email = request.user.email
    data = json.loads(request.body.decode('utf-8'))
    request_email = data['email']
    if user_email == request_email:
        return True
    else:
        return False

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_logged_in(request):
    user_is_valid = check_user_with_token(request)
    data = json.loads(request.body.decode('utf-8'))
    if user_is_valid:
        chat_rooms = request.user.chat_rooms.all().order_by('-last_interaction')
        try:
            if data['chat_room'] == True:
                for room in chat_rooms:
                    room.notice_by_users.add(request.user)
                    room.save()
                chat_rooms = request.user.chat_rooms.all().order_by('-last_interaction')
        finally:
            messages = am.Message.objects.filter(chat_room__in=chat_rooms).order_by('-created')
            return Response({'message': 'Authorized', 'user': aps.UserSerializer(request.user).data,
            'messages': aps.MessageSerializer(messages, many=True).data,
            'chat_rooms': aps.ChatRoomSerializer(chat_rooms, many=True).data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)            

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enter_chat_room(request):
    user_is_valid = check_user_with_token(request)
    data = json.loads(request.body.decode('utf-8'))
    if user_is_valid:
        target_profile_name = data['profile_name']
        target_user = am.AppUser.objects.filter(username = target_profile_name)
        if len(target_user) == 1:
            # room = ChatRoom.objects.filter(Q(users__icontains = request.user) & Q(users__icontains = target_user[0]) & Q(is_group_chat = False))
            rooms = request.user.chat_rooms.all()
            existed_chat_room = None
            for room in rooms:
                if target_user[0] in room.users.all() and room.is_group_chat == False:
                    existed_chat_room = room
                    break
            if existed_chat_room != None:
                return Response({'message': 'Success', 'room': aps.ChatRoomSerializer(existed_chat_room).data}, status=status.HTTP_200_OK)
            else:
                new_room = am.ChatRoom.objects.create()
                new_room.users.add(request.user)
                new_room.users.add(target_user[0])
                new_room.save()
                return Response({'message': 'Created', 'room': aps.ChatRoomSerializer(new_room).data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)