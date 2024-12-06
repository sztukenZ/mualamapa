from django.db import models
from users.models import User
from restaurants.models import Restaurant, Menu

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        limit_choices_to={'user_type': 'customer'}
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    delivery_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries',
        limit_choices_to={'user_type': 'delivery_person'}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    menu_item = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order #{self.order.id})"


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled')
        )
    )
    changed_at = models.DateTimeField(auto_now_add=True)  # Data zmiany statusu
    changed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='status_changes'
    )  # Kto zmienił status

    def __str__(self):
        return f"Order #{self.order.id} status changed to {self.status} at {self.changed_at}"
