from django.db import models
from custom_user.models import User


class Item(models.Model):
    ACTIVE = 'ACTIVE'
    SOLD = 'SOLD'
    ON_SALE = 'ON_SALE'
    TYPES = (
        (ACTIVE, 'ACTIVE'),
        (SOLD, 'SOLD'),
        (ON_SALE, 'ON_SALE'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to='images', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=TYPES, default=ACTIVE)

    def __str__(self):
        return self.name


class ItemOnSale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name
