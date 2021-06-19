import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_api_client(django_user_model):
    admin = django_user_model.objects.create(username='admin', password='something', is_staff=True)
    ad_token, ad_created = Token.objects.get_or_create(user=admin)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {ad_token}')
    return client


@pytest.fixture
def auth_api_client(django_user_model):
    user = django_user_model.objects.create(username='user', password='password', is_staff=False)
    us_token, us_created = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {us_token}')
    return client


@pytest.fixture
def products_factory():
    def func(**kwargs):
        return baker.make("Products", _quantity=20, **kwargs)

    return func


@pytest.fixture
def product_reviews_factory(user, products_factory):
    def func(**kwargs):
        return baker.make("ProductReviews", user=user, _quantity=5, **kwargs)

    return func


@pytest.fixture
def orders_factory():
    def func(**kwargs):
        return baker.make("Orders", _quantity=8, **kwargs)

    return func


@pytest.fixture
def product_collections_factory():
    def func(**kwargs):
        return baker.make("ProductCollections", make_m2m=True, _quantity=3, **kwargs)

    return func
