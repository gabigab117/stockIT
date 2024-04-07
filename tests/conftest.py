import pytest
from landing.models import CompanyPresentation


@pytest.fixture
def presentation():
    return CompanyPresentation.objects.create(title="presentation", text="super texte !")
