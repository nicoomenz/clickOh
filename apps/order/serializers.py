from itertools import product
from rest_framework import serializers

from apps.products.models import Products
from .models import Order, OrderDetail

class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    total_dolar = serializers.SerializerMethodField()

    def get_total(self, instance):
        return instance.total_invoice(instance.order.all())
    
    def get_total_dolar(self, instance):
        return instance.total_dolar(instance.order.all())

    class Meta:
        model = Order
        fields = [
            "id",
            "date_time",
            "total",
            "total_dolar",
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    
    order = OrderSerializer()
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', queryset=Products.objects.all())


    class Meta:
        model = OrderDetail
        fields = [
            "id",
            "order",
            "cuantity",
            "product_id",
        ]


class OrderListWithDetails(serializers.ModelSerializer):

    orders_details = serializers.SerializerMethodField()

    def get_orders_details(self, data):
        order_detail = OrderDetail.objects.filter(order=data.pk)
        serializer = OrderDetailSerializer(instance=order_detail, many=True).data
        return serializer

    class Meta:
        model = Order
        fields = [
            "id",
            "date_time",
            "orders_details",
        ]

class OrderDetailCreateUpdateSerializer(serializers.ModelSerializer):

    order_id = serializers.PrimaryKeyRelatedField(
        source='order', queryset=Order.objects.all())

    product_id = serializers.PrimaryKeyRelatedField(
        source='product', queryset=Products.objects.all())
    
    def validate(self, data):
        if(not OrderDetail.objects.filter(product=data['product'].pk)):
            if(not Products.objects.get(pk=data['product'].pk).stock_value(data['cuantity'])):
                raise serializers.ValidationError(
                    detail={'detail': 'No hay stock suficiente'}
                )
            return data
        else:
            raise serializers.ValidationError(
                    detail={'detail': 'No puede repetirse el producto en la misma orden'}
                )

    class Meta:
        model = OrderDetail
        fields = [
            "id",
            "order_id",
            "cuantity",
            "product_id",
        ]