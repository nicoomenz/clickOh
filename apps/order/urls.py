from rest_framework import routers
from .api import *

router = routers.SimpleRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'orderDetail', OrderDetailViewSet, basename='orderDetail')
urlpatterns = []
urlpatterns += router.urls