# Generated by Django 3.2.4 on 2021-07-06 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('online_shop', '0002_auto_20210706_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productcollectionsproducts',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_list', to='online_shop.productcollections'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='online_shop.orders'),
        ),
    ]
