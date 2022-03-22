from django.shortcuts import render
from rest_framework import viewsets, status

from .services import get_casa

from django.http import JsonResponse, response
from rest_framework.response import Response

from apps.products.models import Products
from .serializers import OrderDetailCreateUpdateSerializer, OrderDetailSerializer, OrderListWithDetails, OrderSerializer
from .models import Order, OrderDetail
from django.db import transaction
from rest_framework.decorators import action


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):

    serializers = {
        'default': OrderSerializer,
        'retrieve': OrderListWithDetails,
    }
    queryset = Order.objects.all()

    def get_serializer_class(self):
        """
        Devuelve un serializador en función del verbo HTTP.
        Si no está definido, devuelve el serializador
        por defecto.
        """

        return self.serializers.get(
            self.action, self.serializers["default"])
    
    @action(detail=True, methods=['GET'], url_path='totalCalculate', url_name="totalCalculate")
    def total_calculate(self, request, *args, **kwargs):
        """ calcular el total de los detalles de una orden """
        instance = self.get_object()
        serializer = OrderSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """ borrar atomicamente en cascada orders, ordersDetails y products """
        with transaction.atomic():
            order = self.get_object()
            order_detail = OrderDetail.objects.get(order=order)
            Products.objects.get(pk=order_detail.product.pk).return_stock(order_detail.cuantity)

        return super().destroy(request, *args, **kwargs)

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializers = {
        'default': OrderDetailSerializer,
        'create': OrderDetailCreateUpdateSerializer,
    }
    

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
            order_detail = self.get_object()
            Products.objects.get(pk=order_detail.product.pk).return_stock(order_detail.cuantity)

        return super().destroy(request, *args, **kwargs)
    
    