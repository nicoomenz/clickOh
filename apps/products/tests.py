from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework import status

import factory

from .models import Products

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "admin"
    password = 123456

    is_staff = False
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        # if 'persona' not in kwargs:
        #     kwargs['persona'] = PersonaHumana.objects.last()
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        # ensure the raw password gets set after the initial save
        obj.set_password(password)
        obj.save()
        return obj

class RFAPIClient(APIClient):
    pass


class RFAPITestCase(APITestCase):
    client_class = RFAPIClient
    user_factory = UserFactory

class ProductsTests(RFAPITestCase):

    def setUp(self):
        self.user = self.user_factory.create(password='123456', is_staff=True, )
        self.client = self.client_class()
        self.client.login(username=self.user.username, password='123456')
    
        self.producto = Products.objects.create(
            name="porotos",
            price=20,
            stock=100
        )
    
    def test_list(self):
        url = reverse('products-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_pk = response.data[0]['name']
        product = Products.objects.get(pk=product_pk)

        self.assertEqual(response.data[0]['name'], product.name)
        self.assertEqual(response.data[0]['stock'], product.stock)
        self.assertEqual(response.data[0]['price'], product.price)
