from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Products(models.Model):
    """ Товары """

    name = models.CharField(max_length=128, verbose_name='Наименование')
    description = models.TextField(default='', verbose_name='Описание')
    price = models.PositiveIntegerField(null=False, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class ProductReviews(models.Model):
    """ Отзывы """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.PositiveIntegerField(default=1,
                                       validators=[MinValueValidator(1), MaxValueValidator(5)],
                                       verbose_name='Оценка'
                                       )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class OrderStatusChoices(models.TextChoices):
    """Статусы заказов"""

    NEW = "NEW ", "Новый"
    IN_PROGRESS = "IN_PROGRESS ", "В процессе"
    DONE = 'DONE', " Завершено"


class Orders(models.Model):
    """ Заказы """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='user',
    )
    cart = models.ManyToManyField(Products, through='ProductOrder', verbose_name='Корзина')
    status = models.CharField(max_length=128,
                              choices=OrderStatusChoices.choices,
                              default=OrderStatusChoices.NEW
                              )
    price_cart = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Товары:{self.cart} на сумму {self.price_cart}'


class ProductOrder(models.Model):
    """ Промежуточная таблица товар-заказ"""

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='positions')


class ProductCollections(models.Model):
    """ Подборки """

    name = models.CharField(max_length=128, verbose_name='Название подборки')
    text = models.TextField()
    products = models.ManyToManyField(Products, through='ProductCollectionsProducts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return self.name


class ProductCollectionsProducts(models.Model):
    """ Промежуточная таблица подборки-товары """

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    collection = models.ForeignKey(ProductCollections, on_delete=models.CASCADE, related_name='products_list')
