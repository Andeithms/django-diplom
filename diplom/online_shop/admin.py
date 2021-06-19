from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    pass


class ProductReviewsAdmin(admin.ModelAdmin):
    pass


class ProductOrderInLine(admin.TabularInline):
    model = ProductOrder


class OrdersAdmin(admin.ModelAdmin):
    inlines = [ProductOrderInLine]


class ProductCollectionsProductsInLine(admin.TabularInline):
    model = ProductCollectionsProducts


class ProductCollectionsAdmin(admin.ModelAdmin):
    inlines = [ProductCollectionsProductsInLine]


admin.site.register(Products, ProductAdmin)
admin.site.register(ProductReviews, ProductReviewsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(ProductCollections, ProductCollectionsAdmin)
