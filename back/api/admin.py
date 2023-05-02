from django.contrib import admin
from .models import Item, ItemOnSale



class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'img', 'initial_price', 'owner')


class ItemOnSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'current_price', 'last_bidder')


admin.site.register(ItemOnSale, ItemOnSaleAdmin)
admin.site.register(Item, ItemAdmin)

