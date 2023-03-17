from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import *
from .models import *


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ItemViewSet(ViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = Item.objects.all()

    def list(self, request):
        serializer = ItemSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def create(self, request):

        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ItemOnSaleViewSet(ViewSet):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = ItemOnSale.objects.all()

    def list(self, request):
        serializer = ItemOnSaleSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ItemOnSale.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemOnSaleSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = ItemOnSaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ItemOnSaleSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
