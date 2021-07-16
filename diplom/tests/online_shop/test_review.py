import random

import pytest
import rest_framework.status as status
from django.urls import reverse


@pytest.mark.django_db
def test_get_review(api_client, product_reviews_factory):
    """ Получение правильного отзыва по id"""
    product_reviews = product_reviews_factory()
    index = random.randrange(5)
    url = reverse("product-reviews-detail", args=[product_reviews[index].id])
    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json["id"] == product_reviews[index].id


@pytest.mark.django_db
def test_list_review(api_client, product_reviews_factory):
    """ Получение всего списка отзывов"""
    product_reviews_factory()
    url = reverse("product-reviews-list")
    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    assert len(resp_json) == 5


@pytest.mark.django_db
def test_user_review(auth_api_client, product_reviews_factory):
    """ Проверка фильтрации по пользователю"""
    product_reviews = product_reviews_factory()
    creator_id = random.choice(product_reviews).user_id
    url = reverse("product-reviews-list")
    resp = auth_api_client.get(url, data={"user": creator_id})
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json[0]["creator"] == creator_id


@pytest.mark.django_db
def test_date_create_review(auth_api_client, product_reviews_factory):
    """ Проверка фильтрации по дате создания"""
    product_reviews = product_reviews_factory()
    date = random.choice(product_reviews).created_at
    url = reverse("product-reviews-list")
    resp = auth_api_client.get(url, data={"created_at": date})
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json[0]["created_at"] == date


@pytest.mark.django_db
def test_id_product_review(auth_api_client, product_reviews_factory):
    """ Проверка фильтрации по id товара"""
    product_reviews = product_reviews_factory()
    product_id = random.choice(product_reviews).product_id.id
    url = reverse("product-reviews-list")
    resp = auth_api_client.get(url, data={"product_id": product_id})
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_200_OK
    # assert resp_json[0]["product_id"] == product_id


@pytest.mark.django_db
def test_create_review_auth(auth_api_client, products_factory, product_reviews_factory):
    """ Проверка на добавление отзыва авторизованным пользователем"""
    product = products_factory()[0]

    url = reverse("product-reviews-list")
    resp = auth_api_client.post(
        url, data={"text": "отзыв", "rate": 1, "product_id":product.id}, format="json"
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json["text"] == "отзыв" and resp_json["product_id"] == product.id


@pytest.mark.django_db
def test_update_review_auth(auth_api_client, product_reviews_factory, user):
    """ Проверка на обновление отзыва авторизованным пользователем"""
    product_reviews = product_reviews_factory()[0]
    product_reviews.user = user

    url = reverse("product-reviews-detail", args=[product_reviews.id])
    resp = auth_api_client.patch(url, data={"text": product_reviews.text})
    resp_json = resp.json()
    print(resp_json)

    assert resp.status_code == status.HTTP_200_OK  # 400
    assert resp_json["text"] == product_reviews.text


@pytest.mark.django_db
def test_update_review_not_auth(api_client, product_reviews_factory, user):
    """ Проверка на обновление отзыва неавторизованным пользователем"""
    product_reviews = product_reviews_factory()[0]
    product_reviews.user = user

    url = reverse("product-reviews-detail", args=[product_reviews.id])
    resp = api_client.patch(url, data={"text": product_reviews.text})

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_review_auth(auth_api_client, product_reviews_factory, user):
    """ Проверка на удаление отзыва авторизованным пользователем"""
    product_reviews = product_reviews_factory()
    index = random.randrange(5)

    url = reverse("product-reviews-detail", args=[product_reviews[index].id])
    resp = auth_api_client.delete(url)

    url_ = reverse("product-reviews-list")
    resp_ = auth_api_client.get(url_)
    resp_json = resp_.json()
    # reviews_id = [product_reviews.id for product_reviews in resp_json]

    assert resp.status_code == status.HTTP_204_NO_CONTENT
    # assert product_reviews[index].id not in reviews_id


@pytest.mark.django_db
def test_delete_review_not_auth(api_client, product_reviews_factory, user):
    """ Проверка на удаление отзыва неавторизованным пользователем"""
    product_reviews = product_reviews_factory()
    index = random.randrange(5)

    url = reverse("product-reviews-detail", args=[product_reviews[index].id])
    resp = api_client.delete(url)

    url_ = reverse("product-reviews-list")
    resp_ = api_client.get(url_)
    resp_json = resp_.json()
    # reviews_id = [product_reviews.id for product_reviews in resp_json]

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    # assert product_reviews[index].id in reviews_id
