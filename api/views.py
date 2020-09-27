import cloudinary.uploader
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

import api.models as am
import api.permissions as ap
import api.serializers as aps


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

#
# class GetUserViewSets(viewsets.ModelViewSet):
#
#     """
#     The user search endpoint searches based on
#     email or username
#     /api/user/filter_user//?s=<value?
#     """
#
#     @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
#     def get_user_with_id(self, request):
#
#         try:
#             params = request.query_params.get('id')
#             user = am.AppUser.objects.get(id=params)
#             serializer = aps.AppUserSerializer(user)
#         except am.AppUser.DoesNotExist:
#             return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.data, status=status.HTTP_200_OK)


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

