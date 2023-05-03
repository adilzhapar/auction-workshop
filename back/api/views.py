from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import ReadOnly
from .serializers import ItemSerializer, ItemCreateSerializer, ItemOnSaleCreateSerializer, ItemOnSaleUpdateSerializer, \
    ItemOnSaleReadSerializer
from .models import Item, ItemOnSale
from .services import ItemOnSaleService


class ItemViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'create':
            return ItemCreateSerializer
        return ItemSerializer

    def get_queryset(self):
        return Item.objects.all()


class ItemOnSaleViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'create':
            return ItemOnSaleCreateSerializer
        if self.action == 'update':
            return ItemOnSaleUpdateSerializer
        return ItemOnSaleReadSerializer

    def get_queryset(self):
        return ItemOnSale.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['last_bidder'] = self.request.user
        obj = serializer.save()
        ItemOnSaleService(self.action, obj).create_item_on_sale()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        ItemOnSaleService(self.action, obj).update_item_on_sale()
        obj.last_bidder = self.request.user
        obj.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
