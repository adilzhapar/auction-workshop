from django.urls import path
from .views import *

urlpatterns = [
    path("items/", ItemViewSet.as_view({"get": "list", "post": "create"})),
    path("items/<int:pk>/", ItemViewSet.as_view({"get": "retrieve"})),
    path("items-on-sale/", ItemOnSaleViewSet.as_view({"get": "list", "post": "create"})),
]