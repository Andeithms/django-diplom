from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('products', ProductsViewSet, 'products')
router.register('product-reviews', ProductReviewsViewSet, 'product-reviews')
router.register('orders', OrdersViewSet, 'orders')
router.register('product-collections', ProductCollectionsViewSet, 'product-collections')


urlpatterns = [] + router.urls
