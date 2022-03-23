from django.db import models
from apps.products.models import Products
from apps.order.services import get_casa
# Create your models here.

class Order(models.Model):
    date_time = models.DateTimeField()

    def total_invoice(self, details):
        sum=0
        for detail in details:
            sum = sum + detail.cuantity
        return sum

    def total_dolar(self, details):
        total_pesos = self.total_invoice(details)
        price_dolar = get_casa()
        if (price_dolar > 0):
            return total_pesos/price_dolar
        else:
            return "no hubo respuesta de apiDolar"



class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    cuantity = models.IntegerField()
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name='product',
    )