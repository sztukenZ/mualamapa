from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant_profile')
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    opening_hours = models.JSONField()
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)


class Menu(models.Model):
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name='menu'
    )
    name = models.CharField(max_length=100)  # Nazwa pozycji w menu
    description = models.TextField()  # Opis pozycji
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Cena
    is_available = models.BooleanField(default=True)  # Dostępność

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

    def clean(self):
        if self.price < 0:
            raise ValidationError("Cena pozycji menu nie może być ujemna.")

    def save(self, *args, **kwargs):
        self.clean()  # Wywołanie walidacji
        super().save(*args, **kwargs)


class Promotion(models.Model):
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name='promotions'
    )
    menu_item = models.ForeignKey(
        'restaurants.Menu',
        on_delete=models.CASCADE,
        related_name='promotions',
        null=True,
        blank=True
    )
    description = models.TextField()  # Opis promocji
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # Zniżka w procentach
    valid_until = models.DateTimeField()  # Data ważności promocji

    def __str__(self):
        return f"Promotion for {self.restaurant.name} - {self.discount}% off"

    def clean(self):
        if self.valid_until <= now():
            raise ValidationError("Promocja nie może mieć daty ważności w przeszłości.")

    def save(self, *args, **kwargs):
        self.clean()  # Wywołanie walidacji
        super().save(*args, **kwargs)



class Review(models.Model):
    customer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews',
        limit_choices_to={'user_type': 'customer'}
    )
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField()  # Ocena (1-5)
    comment = models.TextField(null=True, blank=True)  # Opcjonalny komentarz
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.restaurant.name} by {self.customer.username} - {self.rating}/5"
