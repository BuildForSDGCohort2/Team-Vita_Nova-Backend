import cloudinary.uploader
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

import api.models as am
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
        the the body
        of the request
        """

        url = ''
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
