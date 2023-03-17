from rest_framework import serializers
from django.core.mail import send_mail
from .models import *
from custom_user.models import User
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Item.objects.create(**validated_data)

    owner = UserSerializer()

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'img', 'owner', 'initial_price', 'status')


class ItemOnBidSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Item
        fields = ('name', 'description', 'img', 'owner')


class ItemOnSaleSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['current_price'] < attrs['item'].initial_price:
            raise serializers.ValidationError({"current_price": "Current price must be greater than initial price."})
        if attrs['last_bidder'] == attrs['item'].owner:
            raise serializers.ValidationError({"last_bidder": "Last bidder cannot be the owner."})
        attrs['item'].status = Item.ON_SALE
        return attrs

    def create(self, validated_data):
        send_mail(
            'Your item is on sale!',
            validated_data['item'].name + ' is on sale!' + ' Current price: ' + str(validated_data['current_price']),
            settings.DEFAULT_FROM_EMAIL,
            [validated_data['item'].owner.email],
            fail_silently=False,
        )
        current_item = ItemOnSale.objects.create(**validated_data)
        current_item.save()
        return current_item

    # item = ItemSerializer()
    # current_bidder = UserSerializer(read_only=True, source='last_bidder')

    class Meta:
        model = ItemOnSale
        fields = ('item', 'current_price', 'last_bidder')
