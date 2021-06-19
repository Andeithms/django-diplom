from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Products, Orders, ProductReviews, ProductCollections
from .serializers import ProductSerializer, ProductReviewsSerializers, OrdersSerializer, ProductCollectionsSerializer
from .filters import *
from .permissions import AccessPermission, AdminAccessPermission


class ProductsViewSet(ModelViewSet):
    """ViewSet для товаров."""

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Products.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), AdminAccessPermission()]
        return []

    # def perform_create(self, serializer):



class OrdersViewSet(ModelViewSet):
    """ViewSet для заказов."""

    serializer_class = OrdersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrdersFilter

    def get_queryset(self):
        return Orders.objects.prefetch_related('positions').filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), AccessPermission()]
        return []

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)


class ProductReviewsViewSet(ModelViewSet):
    """ViewSet для отзывов."""

    serializer_class = ProductReviewsSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductReviewsFilter

    def get_queryset(self):
        return ProductReviews.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), AccessPermission()]
        return []

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)


class ProductCollectionsViewSet(ModelViewSet):
    """ViewSet для подборок."""

    serializer_class = ProductCollectionsSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return ProductCollections.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), AccessPermission()]
        return []

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)