import pytest
import random
from django.urls import reverse
import rest_framework.status as status


@pytest.mark.django_db
def test_get_collection(auth_api_client, product_collections_factory):
    """ Получение подборки по id"""
    collections = product_collections_factory()
    index = random.randrange(3)
    url = reverse("product-collections-detail", args=[collections[index].id])
    resp = auth_api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json["id"] == collections[index].id


@pytest.mark.django_db
def test_get_all_collection(api_client, product_collections_factory):
    """ Получение всех подборок"""
    product_collections_factory()
    url = reverse("product-collections-list")
    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert resp_json["id"] == 3


@pytest.mark.django_db
def test_create_collection_admin(admin_api_client, product_collections_factory, products_factory):
    """ Создание подборки админом"""
    product = products_factory()[0]
    url = reverse("product-collections-list")

    resp = admin_api_client.post(url, data={"name": "подборка машин",
                                            "text": "audi",
                                            "products": product.id}, format="json")
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json["name"] == "подборка машин"
    assert resp_json["text"] == "audi"
    assert resp_json["products"] == product.id


@pytest.mark.django_db
def test_create_collection_user(auth_api_client, product_collections_factory, products_factory):
    """ Создание подборки пользователем"""
    product = products_factory()[0]
    url = reverse("product-collections-list")

    resp = auth_api_client.post(url, data={"name": "подборка машин",
                                           "text": "audi",
                                           "products": product.id}, format="json")

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_collection_admin(admin_api_client, product_collections_factory):
    """ Создание подборки админом"""
    collections = product_collections_factory()
    index = random.randrange(3)

    url = reverse("product-collections-detail", args=[collections[index].id])
    resp = admin_api_client.delete(url)

    assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_collection_user(auth_api_client, product_collections_factory):
    """ Создание подборки пользователем"""
    collections = product_collections_factory()
    index = random.randrange(3)

    url = reverse("product-collections-detail", args=[collections[index].id])
    resp = auth_api_client.delete(url)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
