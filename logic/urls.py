from django.conf.urls import include
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from rest_framework import routers
from rest_framework.routers import DefaultRouter
import logic.views as lv

router = DefaultRouter(trailing_slash=False)
app_router = routers.DefaultRouter()
app_router.register('distributor', lv.DistributorViewSet, 'distributor')
app_router.register('sender', lv.SenderViewSet, basename='sender')

urlpatterns = [
    path('', include(app_router.urls)),
]
