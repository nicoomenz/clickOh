from rest_framework import routers
from .api import *

router = routers.SimpleRouter()
router.register(r'products', ProductsViewSet, basename='products')
urlpatterns = []
urlpatterns += router.urls