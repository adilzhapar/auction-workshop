from django.contrib import admin
from .models import Item, ItemOnSale

admin.site.register(Item)


class ItemOnSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'current_price', 'last_bidder')


admin.site.register(ItemOnSale, ItemOnSaleAdmin)
