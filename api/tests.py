import api.models as am
from django.test import TestCase
from rest_framework.test import APIClient


class UserViewSetCRUD(TestCase):
    """Test module for the CreateUser viewset"""

    def setUp(self):
        self.client = APIClient()

        test_user_1 = am.AppUser.objects.create(
            email="test_user_1@lamp.hub"
        )
        test_user_2 = am.AppUser.objects.create(
            email="test_user_2@lamp.hut",
            password="blablablabla"
        )
        test_user_3 = am.AppUser.objects.create(
            email="test_user_3@lamp.hut",
            password="blablablabla"
        )
        test_user_4 = am.AppUser.objects.create(
            email="test_user_4@lamp.hut",
            password="blablablabla"
        )
        test_user_5 = am.AppUser.objects.create(
            email="test_user_5@lamp.hut",
            password="blablablabla"
        )

