from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductsCreateUpdateSerializer, ProductsSerializer
from .models import Products
from apps.order.models import Order, OrderDetail
from django.db import transaction

# Create your views here.
class ProductsViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': ProductsSerializer,
        'create': ProductsSerializer,
        'update': ProductsCreateUpdateSerializer,
        'partial_update': ProductsCreateUpdateSerializer,
    }
    queryset = Products.objects.all()

    def get_serializer_class(self):
        """
        Devuelve un serializador en función del verbo HTTP.
        Si no está definido, devuelve el serializador
        por defecto.
        """

        return self.serializers.get(
            self.action, self.serializers["default"])
    
    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            product_destroy = self.get_object()
            orders_of_product = OrderDetail.objects.filter(product=product_destroy.pk)
            for i in orders_of_product:
                Order.objects.get(pk=i.pk).delete()          

        return super().destroy(request, *args, **kwargs)