from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import serializers
from .models import Products, Orders, ProductReviews, ProductCollections, ProductOrder


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для товаров """

    class Meta:
        model = Products
        fields = ('id', 'name', 'description', 'price',
                  'created_at', 'updated_at',)


class ProductReviewsSerializers(serializers.ModelSerializer):
    """Serializer для отзывов """

    user = serializers.IntegerField(read_only=True, source='user.id')

    class Meta:
        model = ProductReviews
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, attrs):
        user = self.context['request'].user

        if self.context['view'].action == 'create':
            if ProductReviews.objects.filter(user=user, product_id=attrs['product_id']):
                raise ValidationError(f'Нельзя оставлять более одного отзыва к каждому товару')
            attrs['user'] = user

        elif self.context['view'].action in ['update', 'partial_update']:
            fields = ('text', 'rate',)
            if not set(attrs.keys()).issubset(fields):
                raise ValidationError(f'Изменить можно только поля {fields}')

        return attrs


class ProductOrderSerializer(serializers.Serializer):
    """Serializer для positions в заказах """

    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=True, )

    quantity = serializers.IntegerField(min_value=1, default=1)


class OrdersSerializer(serializers.ModelSerializer):
    """Serializer для заказов """

    positions = ProductOrderSerializer(many=True)

    class Meta:
        model = Orders
        fields = ('id', 'status', 'cart', 'created_at', 'updated_at', 'positions')

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["user"] = self.context["request"].user
        positions = validated_data.pop('positions')
        for item in positions:
            ProductOrder(product=item['product'],
                         quantity=item['quantity'],
                         order=super().create(validated_data)
                         ).save()

        return super().create(validated_data)

    def validate(self, value):
        user = self.context['request'].user
        if self.context['view'].action == 'create':
            positions = value["positions"]
            if not positions:
                raise serializers.ValidationError("Не указаны позиции заказа")
            product_ids = [item["product"].id for item in positions]
            if len(product_ids) != len(set(product_ids)):
                raise serializers.ValidationError("Дублируются позиции в заказе")

            price_cart = sum(item['product'].price * item['quantity'] for item in positions)
            value['user'] = user
            value['price_cart'] = price_cart

        elif self.context['view'].action in ['update', 'partial_update']:
            if user.is_staff:
                fields = ('status', 'positions',)
            else:
                fields = ('positions',)
            if not set(value.keys()).issubset(fields):
                raise ValidationError(f'Изменить можно только поля {fields}')

        return value

    def update(self, instance, validated_data):
        positions = validated_data.get('positions', [])
        for item in positions:
            try:
                cart = ProductOrder.objects.get(product_id=item['product']['id'].id,
                                                order=instance
                                                )
                cart.quantity = item['quantity']
                cart.save()
            except ObjectDoesNotExist:
                self.create(validated_data)

        value = ProductOrder.objects.filter(order=instance)
        price_cart = sum([item.product.price * item.quantity for item in value])
        if price_cart > 0:
            validated_data['price_cart'] = price_cart

        return super().update(instance, validated_data)


class ProductCollectionsProductsSerializer(serializers.Serializer):
    """Serializer для products в подборках """

    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=True)
    name = serializers.CharField(source='products.name', required=True)
    price = serializers.CharField(source='products.price', required=True)


class ProductCollectionsSerializer(serializers.ModelSerializer):
    """Serializer для подборок """

    products = ProductCollectionsProductsSerializer(many=True, required=True)
    user = serializers.IntegerField(read_only=True, source='user.id')

    class Meta:
        model = ProductCollections
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products_list')
        for item in products:
            Products(id=item['product'].id).save()

        return super().create(validated_data)

    def validate(self, attrs):
        products = attrs.get('products_list')
        attrs["user"] = self.context['request'].user
        if self.context['view'].action == 'create':
            if not products:
                raise serializers.ValidationError("Не указаны товары")
            product_ids = [item["product"].id for item in products]
            if len(product_ids) != len(set(product_ids)):
                raise serializers.ValidationError("Дублируются позиции в подборке")
        return attrs

    def update(self, instance, validated_data):
        products = validated_data.get('products_list')
        all_products = instance.products.all()
        for item in products:
            if item['product'] not in all_products:
                instance.products.add(item['product'])

        return super().update(instance, validated_data)
