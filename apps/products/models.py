from enum import unique
from django.db import models
from django.db import transaction

# Create your models here.

class Products(models.Model):

    name = models.TextField(primary_key=True)
    price = models.FloatField()
    stock = models.IntegerField()
    

    def stock_value(self, orderCant):
        if(self.stock>orderCant):
            self.stock=self.stock-orderCant      
            self.save()
            return True
        else:
            return False
    
    def return_stock(self, orderCant):
        with transaction.atomic():
            self.stock=self.stock+orderCant
            self.save()
            return True
        return False
