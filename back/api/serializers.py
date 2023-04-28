from rest_framework import serializers
from .models import *
from custom_user.models import User
from celery import shared_task
from .tasks import item_sold, send_notification_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ItemCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    class Meta:
        model = Item
        fields = ('name', 'description', 'img', 'owner', 'initial_price', 'status')


class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'img', 'owner', 'initial_price', 'status')


class ItemOnSaleSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['current_price'] < attrs['item'].initial_price:
            raise serializers.ValidationError({"current_price": "Current price must be greater than initial price."})
        if attrs['last_bidder'] == attrs['item'].owner:
            raise serializers.ValidationError({"last_bidder": "Last bidder cannot be the owner."})
        same_item_on_sale = ItemOnSale.objects.filter(item=attrs['item']).count()
        if same_item_on_sale >= 1:
            raise serializers.ValidationError({"item": "This item is already on sale."})

        return attrs

    def create(self, validated_data):

        send_notification_email.delay('Your item is on sale!',
                                      validated_data['item'].name + ' is on sale!' + ' Current price: ' + str(
                                          validated_data['current_price']),
                                      validated_data['item'].owner.email
                                      )

        item_key = validated_data['item'].id
        item = Item.objects.get(id=item_key)
        item.status = Item.ON_SALE
        item.save()

        current_item = ItemOnSale.objects.create(**validated_data)
        current_item.save()

        item_sold.apply_async(args=[current_item.id], countdown=30)
        return current_item

    @shared_task(bind=True)
    def update(self, instance, validated_data):
        if instance.current_price >= validated_data['current_price']:
            raise serializers.ValidationError({"current_price": "New price must be greater than previous price."})

        send_notification_email.delay(
            'Your bid was intercepted!',
            validated_data['item'].name + ' Current price: ' + str(validated_data['current_price']),
            validated_data['item'].owner.email
        )
        return super().update(instance, validated_data)

    class Meta:
        model = ItemOnSale
        fields = ('item', 'current_price', 'last_bidder')


class ItemOnSaleReadSerializer(ItemOnSaleSerializer):
    item = ItemSerializer(read_only=True)
    last_bidder = UserSerializer(read_only=True)

    class Meta:
        model = ItemOnSale
        fields = ('id', 'item', 'current_price', 'last_bidder')
