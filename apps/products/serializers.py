from rest_framework import serializers
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = [
            "name",
            "price",
            "stock",
        ]

class ProductsCreateUpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        return instance

    class Meta:
        model = Products
        fields = [
            "price",
            "stock",
        ]