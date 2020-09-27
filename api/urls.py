from django.conf.urls import include
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from rest_framework import routers
from rest_framework.routers import DefaultRouter
import api.views as av

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register('', av.UserViewSets, 'user')
app_router.register('profile', av.ProfileViewSet, basename='profile')
app_router.register('review', av.UserReviewViewSet, basename='review')
# app_router.register('user', av.GetUserViewSets, basename='user')

urlpatterns = [

    path('accounts/', include('rest_registration.api.urls')),
    path('token/jwt', av.CustomTokenObtainPairView.as_view()),
    path('token/jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(app_router.urls)),
]
