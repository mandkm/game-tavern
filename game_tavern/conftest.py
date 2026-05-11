import pytest
from django.urls import reverse

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def create_user(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    def make_user(**kwargs):
        return User.objects.create(**kwargs)
    return make_user