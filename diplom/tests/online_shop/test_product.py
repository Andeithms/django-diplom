import pytest
import random
from django.urls import reverse
import rest_framework.status as status


@pytest.mark.django_db
def test_get_product(api_client, products_factory):
    """ Получение правильного товара по id"""
    products = products_factory()
    index = random.randrange(15)
    url = reverse("products-detail", args=[products[index].id])
    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json["id"] == products[index].id


@pytest.mark.django_db
def test_list_product(api_client, products_factory):
    """ Получение всего списка товаров"""
    products_factory()
    url = reverse("products-list")
    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_json) == 20


@pytest.mark.django_db
def test_name_product(api_client, products_factory):
    """ Проверка фильтрации по названию"""
    products = products_factory()
    name = random.choice(products).name
    url = reverse("products-list")
    resp = api_client.get(url, data={"name": name})
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json[0]["name"] == name


@pytest.mark.django_db
def test_description_product(api_client, products_factory):
    """ Проверка фильтрации по описанию"""
    products = products_factory()
    description = random.choice(products).description
    url = reverse("products-list")
    resp = api_client.get(url, data={"description": description})
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json[0]["description"] == description


@pytest.mark.django_db
def test_price_product(api_client, products_factory):
    """ Проверка фильтрации по цене"""
    products = products_factory()
    price = random.choice(products).price
    url = reverse("products-list")
    resp = api_client.get(url, data={"price_min": price, "price_max": price})
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json[0]["price"] == price


@pytest.mark.django_db
def test_create_product_admin(admin_api_client, products_factory):
    """ Проверка на добавление товара админом"""
    url = reverse("products-list")
    resp = admin_api_client.post(url, data={"name": "тестовый товар",
                                            "description": "описание",
                                            "price": 300}, format="json")
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json['name'] == 'тестовый товар'


@pytest.mark.django_db
def test_create_product_user(auth_api_client, products_factory):
    """ Проверка на добавление товара авторизованным пользователем"""
    url = reverse("products-list")
    resp = auth_api_client.post(url, data={"name": "тестовый товар",
                                           "description": "описание",
                                           "price": 300}, format="json")

    assert resp.status_code == status.HTTP_403_FORBIDDEN
