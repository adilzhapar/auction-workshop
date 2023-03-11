from django.db import models
from custom_user.models import User


class Item(models.Model):
    ACTIVE = 'ACTIVE'
    SOLD = 'SOLD'
    TYPES = (
        (ACTIVE, 'ACTIVE'),
        (SOLD, 'SOLD')
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to='media/images')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_price = models.DecimalField(decimal_places=2)
    status = models.CharField(max_length=10, choices=TYPES, default=ACTIVE)

    def __str__(self):
        return self.name

