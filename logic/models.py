from django.db import models
from api.models import AppUser

# Create your models here.
MODE_OF_TRAVEL = (
    ('Commercial', 'Commercial'),
    ('Private', 'Private')
)

GOODS_CATEGORY = (
    ('Cash crop', 'Cash crop'),
    ('Vegetable', 'Vegetable'),
    ('Fruits', 'Fruits')
)

STATUS = (
    ('Open', 'Open'),
    ('Close', 'Close')
)


class Distributor(models.Model):
    active_distributor = models.BooleanField(max_length=20, default=False)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='distributor_user', null=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    purpose_of_travel = models.TextField(max_length=500, null=True)
    active_contact_number = models.CharField(max_length=20)
    mode_of_travel = models.CharField(max_length=100, choices=MODE_OF_TRAVEL)
    additional_comment = models.TextField(max_length=500, blank=True, null=True)
    travel_schedule = models.DateTimeField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, default="Open")

    def __str__(self):
        return self.departure + " ==> " + self.destination + " by " \
               + self.travel_schedule.strftime('%d-%m-%Y %H:%M:%S')


class Sender(models.Model):
    goods_image = models.TextField(null=True, default='')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sender_user', null=True)
    booked_distributor = models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.CASCADE)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    delivery_contact_number = models.CharField(max_length=20)
    goods_category = models.CharField(max_length=100, choices=GOODS_CATEGORY)
    description_of_goods = models.TextField(max_length=500, blank=True, null=True)
    travel_schedule = models.DateTimeField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, default="Open")
    accepted_terms = models.BooleanField(max_length=20, default='', null=True)

    def __str__(self):
        return self.departure + " to " + self.destination + " by " + self.travel_schedule.strftime('%d-%m-%Y %H:%M:%S')
