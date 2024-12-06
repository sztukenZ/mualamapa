from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.gis.db.models import PointField


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
        ('delivery_person', 'Delivery Person'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)


class DeliveryPersonProfile(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='delivery_profile'
    )
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('available', 'Available'),
            ('unavailable', 'Unavailable')
        ),
        default='unavailable'
    )
    location = PointField(null=True, blank=True, default=None)

    def __str__(self):
        return f"Delivery Person: {self.user.username}, Status: {self.status}"


