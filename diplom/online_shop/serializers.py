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


class ProductReviewsSerializers(serializers.Serializer):
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
            if ProductReviews.objects.filter(user=user, product=attrs['product']):
                raise ValidationError(f'Нельзя оставлять более одного отзыва к каждому товару')
            attrs['user'] = user

        elif self.context['view'].action in ['update', 'partial_update']:
            fields = ('text', 'rate',)
            if set(attrs.keys()) != fields:
                raise ValidationError(f'Изменить можно только поля {fields}')


class ProductOrderSerializer(serializers.Serializer):
    """Serializer для positions в заказах """

    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=True, )

    quantity = serializers.IntegerField(min_value=1, default=1)


class OrdersSerializer(serializers.ModelSerializer):
    """Serializer для заказов """

    positions = ProductOrderSerializer(many=True)

    class Meta:
        model = Orders
        fields = ('id', 'user', 'status', 'cart', 'price_cart',
                  'created_at', 'updated_at',)

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        positions = validated_data.pop('positions')
        for item in positions:
            ProductOrder(product=item['product'].id,
                         quantity=item['quantity'],
                         order=super().create(validated_data)
                         ).save()

        return super().create(validated_data)

    def validate_positions(self, value):
        user = self.context['request'].user
        if self.context['view'].action == 'create':
            if not value:
                raise serializers.ValidationError("Не указаны позиции заказа")
            product_ids = [item["product"].id for item in value]
            if len(product_ids) != len(set(product_ids)):
                raise serializers.ValidationError("Дублируются позиции в заказе")

            price_cart = sum([item['product']['id'].price * item['quantity'] for item in value])
            value['user'] = user
            value['price_cart'] = price_cart

        elif self.context['view'].action in ['update', 'partial_update']:
            if user.is_staff:
                fields = ('status', 'positions',)
            else:
                fields = ('positions',)
            if set(value.keys()) != fields:
                raise ValidationError(f'Изменить можно только поля {fields}')

        return value

    def update(self, instance, validated_data):
        positions = validated_data.get('positions')
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
        price_cart = sum([item['product']['id'].price * item['quantity'] for item in value])
        validated_data['price_cart'] = price_cart

        return super().update(instance, validated_data)


class ProductCollectionsProductsSerializer(serializers.Serializer):
    """Serializer для products в подборках """

    product = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), required=True, )


class ProductCollectionsSerializer(serializers.Serializer):
    """Serializer для подборок """

    products = ProductCollectionsProductsSerializer(many=True)

    class Meta:
        model = ProductCollections
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        print(validated_data)
        for item in products:
            Products(id=item['product'].id).save()

        return super().create(validated_data)

    def validate(self, attrs):
        products = attrs.get('products')
        if self.context['view'].action == 'create':
            if not products:
                raise serializers.ValidationError("Не указаны товары")
            product_ids = [item["product"].id for item in products]
            if len(product_ids) != len(set(product_ids)):
                raise serializers.ValidationError("Дублируются позиции в подборке")

    def update(self, instance, validated_data):
        products = validated_data.get('products')
        all_products = instance.products.all()
        for item in products:
            if item['product'] not in all_products:
                instance.products.add(item['product'])

        return super().update(instance, validated_data)