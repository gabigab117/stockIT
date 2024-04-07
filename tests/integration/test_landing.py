import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_index(client: Client, presentation):
    response = client.get(reverse("index"))
    assert response.status_code == 200
