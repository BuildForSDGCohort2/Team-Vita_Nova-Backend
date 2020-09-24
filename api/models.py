# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

import uuid

REVIEW_TYPE = (
    ('Sender Review', 'Sender Review'),
    ('Distributor Review', 'Distributor Review')
)


class UserManager(BaseUserManager):

    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        """Create and save a regular User with the given email and password."""

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AppUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, default="", unique=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    completed_distributions = models.IntegerField(null=True)
    completed_send_orders = models.IntegerField(null=True)
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    image = models.TextField(null=True,
                             default='https://res.cloudinary.com/dkozdkklg/image/upload/v1565557753/cloudinary_qyi649'
                                     '.jpg')
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserReview(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='user')
    comment = models.TextField(max_length=500)
    type_of_review = models.CharField(max_length=100, choices=REVIEW_TYPE)
    reviewer = models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class ChatRoom(models.Model):
    users = models.ManyToManyField(AppUser, related_name='chat_rooms')
    notice_by_users = models.ManyToManyField(AppUser, related_name = 'chat_room_noticed')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')
    is_group_chat = models.BooleanField(default = False)
    last_interaction = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name = 'messages')
    read_by_users = models.ManyToManyField(AppUser, related_name = 'read_messages')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content