from rest_framework import serializers
from .models import *
from custom_user.models import User


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


class ItemOnSaleCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['current_price'] < attrs['item'].initial_price:
            raise serializers.ValidationError({"current_price": "Current price must be greater than initial price."})
        if attrs['item'].status == Item.SOLD:
            raise serializers.ValidationError({"item": "This item is already sold."})
        if self.context['request'].user == attrs['item'].owner:
            raise serializers.ValidationError({"last_bidder": "Last bidder cannot be the owner."})
        same_item_on_sale = ItemOnSale.objects.filter(item=attrs['item']).count()
        if same_item_on_sale >= 1:
            raise serializers.ValidationError({"item": "This item is already on sale."})

        return attrs

    class Meta:
        model = ItemOnSale
        fields = ('item', 'current_price')


class ItemOnSaleUpdateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.context['request'].user == self.instance.item.owner:
            raise serializers.ValidationError({"last_bidder": "Last bidder cannot be the owner."})
        if self.instance.current_price >= attrs['current_price']:
            raise serializers.ValidationError({"current_price": "New price must be greater than previous price."})

        return attrs

    class Meta:
        model = ItemOnSale
        fields = ('current_price',)


class ItemOnSaleReadSerializer(ItemOnSaleCreateSerializer):
    item = ItemSerializer(read_only=True)
    last_bidder = UserSerializer(read_only=True)

    class Meta:
        model = ItemOnSale
        fields = ('id', 'item', 'current_price', 'last_bidder')
