from api.models import Item
from .tasks import item_sold, send_notification_email


class ItemOnSaleService:
    def __init__(self, action, item_on_sale):
        self.action = action
        self.item_on_sale = item_on_sale

    def wrap_data(self):
        return {
            'action': self.action,
            'item_name': self.item_on_sale.item.name,
            'item_cur_price': self.item_on_sale.current_price,
            'item_last_bidder_name': self.item_on_sale.last_bidder.first_name,
            'item_owner_email': self.item_on_sale.item.owner.email
        }

    def create_item_on_sale(self):
        self.item_on_sale.item.status = Item.ON_SALE
        self.item_on_sale.item.save()
        data = self.wrap_data()
        send_notification_email.delay(**data)
        item_sold.apply_async(args=[self.item_on_sale.id, self.item_on_sale.current_price], countdown=15)

    def update_item_on_sale(self):
        data = self.wrap_data()
        send_notification_email.delay(**data)
        item_sold.apply_async(args=[self.item_on_sale.id, self.item_on_sale.current_price], countdown=200)
