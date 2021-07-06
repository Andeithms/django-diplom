from django_filters import rest_framework as filters

from .models import Products, Orders, ProductReviews


class ProductFilter(filters.FilterSet):
    """Фильтр товаров """

    name = filters.CharFilter(field_name='name')
    description = filters.CharFilter(field_name='description')
    price = filters.RangeFilter(field_name='price')

    class Meta:
        model = Products
        fields = ('name', 'description', 'price',)


class ProductReviewsFilter(filters.FilterSet):
    """ Фильтр отзывов """

    user_id = 'user__id'
    product_id = filters.NumberFilter(field_name='product_id')
    created_at = filters.DateFromToRangeFilter(field_name='release_date')

    class Meta:
        model = ProductReviews
        fields = ('user', 'product_id', 'created_at',)


class OrdersFilter(filters.FilterSet):
    """ Фильтр заказов """

    product_id = filters.NumberFilter(field_name='product_id')
    price_cart = filters.NumberFilter(field_name='price_cart')
    created_at = filters.DateFromToRangeFilter(field_name='release_date')
    updated_at = filters.DateFromToRangeFilter(field_name='updated_date')

    class Meta:
        model = Orders
        fields = ('status', 'price_cart', 'created_at', 'updated_at',)
