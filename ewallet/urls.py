from django.urls import path

from django.conf.urls import include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
import ewallet.views as ewv

router = DefaultRouter()
router.register('my-accounts',ewv.EwalletViewSets, basename='my-accounts')

urlpatterns = [
    path('', include(router.urls))
]
