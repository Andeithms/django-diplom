import pytest
import random
from django.urls import reverse
import rest_framework.status as status


@pytest.mark.django_db
def test_get_order(auth_api_client, orders_factory):
    """ Получение правильного заказа по id"""
    order = orders_factory()
    index = random.randrange(8)
    url = reverse("orders-detail", args=[order[index].id])
    resp = auth_api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json["id"] == order[index].id


@pytest.mark.django_db
def test_get_all_order(auth_api_client, orders_factory):
    """ Получение правильного всех заказов"""
    orders_factory()
    url = reverse("orders-list")
    resp = auth_api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_json) == 8


@pytest.mark.django_db
def test_status_order(admin_api_client, orders_factory):
    """ Проверка фильтрации по статусу"""
    orders = orders_factory()
    status_ = random.choice(orders).status
    url = reverse("orders-list")
    resp = admin_api_client.get(url, data={"status": status_})
    # ids = {order.id for order in resp.json()}
    right_status = set()
    for order in orders:
        if order.status == status_:
            right_status.add(order.id)

    assert resp.status_code == status.HTTP_200_OK
    # assert ids == right_status


@pytest.mark.django_db
def test_price_order(auth_api_client, orders_factory):
    """ Проверка фильтрации по цене"""
    orders = orders_factory()
    price_cart = random.choice(orders).price_cart
    url = reverse("orders-list")
    resp = auth_api_client.get(url, data={"price_min": price_cart, "price_max": price_cart})
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json[0]["price_cart"] == price_cart


@pytest.mark.django_db
def test_date_create_order(auth_api_client, orders_factory):
    """ Проверка фильтрации по дате создания"""
    orders = orders_factory()
    created_at = random.choice(orders).created_at
    url = reverse("orders-list")
    resp = auth_api_client.get(url, data={"created_at": created_at}, format="json")
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json[0]["created_at"] == created_at


@pytest.mark.django_db
def test_date_update_order(auth_api_client, orders_factory):
    """ Проверка фильтрации по дате обновления"""
    orders = orders_factory()
    update_at = random.choice(orders).updated_at
    url = reverse("orders-list")
    resp = auth_api_client.get(url, data={"updated_at": update_at}, format="json")
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json[0]["update_at"] == update_at


@pytest.mark.django_db
def test_product_order(auth_api_client, orders_factory, products_factory):
    """ Проверка фильтрации по товарам"""
    orders = orders_factory()
    product_id = random.choice(products_factory()).id
    url = reverse("orders-list")
    resp = auth_api_client.get(url, data={"positions": [{"product_id": product_id, "quantity": 1}]}, format="json")
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json[0]["id"] == orders.id


@pytest.mark.django_db
def test_create_order_auth(auth_api_client, orders_factory, products_factory):
    """ Проверка создания заказа авторизованным пользователем"""
    orders = orders_factory()
    product_id = random.choice(products_factory()).id

    url = reverse("orders-list")
    resp = auth_api_client.post(url, data={"positions": [{"product": product_id, "quantity": 1}]}, format="json")
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_order_not_auth(api_client, orders_factory, products_factory):
    """ Проверка создания заказа неавторизованным пользователем"""
    orders = orders_factory()
    product_id = random.choice(products_factory()).id

    url = reverse("orders-list")
    resp = api_client.post(url, data={"positions": [{"product_id": product_id, "quantity": 1}]}, format="json")
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_status_order_auth(auth_api_client, orders_factory):
    """ Проверка обновления заказа авторизованным пользователем"""
    order = orders_factory()[0]
    url = reverse("orders-detail", args=[order.id])
    resp = auth_api_client.patch(url, data={"status":"DONE"}, format="json")

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_status_order_admin(admin_api_client, orders_factory):
    """ Проверка обновления заказа админом"""
    order = orders_factory()[0]
    url = reverse("orders-detail", args=[order.id])
    resp = admin_api_client.patch(url, data={"status":"DONE"}, format="json")

    assert resp.status_code == status.HTTP_200_OK

