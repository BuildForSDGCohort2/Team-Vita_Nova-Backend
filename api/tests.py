from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

import api.models as am
from api.views import ProfileViewSet, UserReviewViewSet


class TestUserProfile(TestCase):

    """
    Test module for the UserProfile ViewSet
    """

    def setUp(self):
        self.client = APIClient()
        try:
            self.test = ProfileViewSet()
        except NameError as e:
            pass
        am.AppUser.objects.create(
            email='test_user1@vitanova.com',
            password='test_password',
        )
        am.AppUser.objects.create(
            email='test_user2@vitanova.com',
            password='test_password',
        )

    def testProfileViewSetClassExists(self):
        # Check if ProfileViewSet Class Exists
        self.assert_(self.test is not None)

    def test_get_user_profile(self):
        user = am.AppUser.objects.get(email='test_user1@vitanova.com')
        user1 = am.AppUser.objects.get(email='test_user2@vitanova.com')

        # authenticated and account owner
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("profile-get-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user)
        self.assertNotContains(response, user1)
        self.client.force_authenticate(user=None)

        # authenticated but not account owner
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("profile-get-profile"), {'email': user1.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)

        # non authenticated users
        response = self.client.get(reverse('profile-get-profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=None)

    def test_update_user_profile(self):
        test_user2 = am.AppUser.objects.get(email='test_user1@vitanova.com')
        data = {
            "username": "create88k",
            "address": "81 lagos street",
            "state": "Lagos",
            "region": "South West",
            "country": "Nigeria",
            "phone_number": "08921345667"
        }

        # authenticated and owner
        self.client.force_authenticate(user=test_user2)
        response = self.client.patch(reverse("profile-update-profile"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)

        # non authenticated user
        response = self.client.patch(reverse("profile-update-profile"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=None)


class TestUserReviewViewSet(TestCase):

    """
    Test modules for User Review
    """

    def setUp(self):
        self.client = APIClient()
        try:
            self.test = UserReviewViewSet()
        except NameError as e:
            print(e)
            pass

        test_user = am.AppUser.objects.create(
            email='test_user1@vitanova.com',
            password='test_password',
        )
        test_user1 = am.AppUser.objects.create(
            email='test_user2@vitanova.com',
            password='test_password',
        )

        am.UserReview.objects.create(user=test_user, type_of_review='Sender Review',
                                     comment='A nice guy', rating=4.3, reviewer=test_user1)

    def testUserReviewClassExists(self):
        # Check if UserReview Class Exists
        self.assert_(self.test is not None)

    def test_get_user_reviews(self):
        user = am.AppUser.objects.get(email='test_user1@vitanova.com')
        user2 = am.AppUser.objects.get(email='test_user2@vitanova.com')

        # authenticated and account owner
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("review-get-user-review"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)

        # authenticated but not account owner
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("review-get-user-review"), {'user': user2.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)

        # non authenticated users
        response = self.client.get(reverse('review-get-user-review'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=None)

    def test_post_user_review(self):
        data = {
            "comment": "A nice guy",
            "type_of_review": "Sender Review",
            "rating": 4.6,
            "user": 2
        }

        # Check post with unauthenticated user
        response = self.client.post(reverse("review-post-user-review"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=None)
