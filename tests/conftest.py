import pytest
from account.models import CustomUser
from landing.models import CompanyPresentation


@pytest.fixture
def presentation():
    return CompanyPresentation.objects.create(title="presentation", text="super texte !")


@pytest.fixture
def user_1():
    return CustomUser.objects.create_user(email="gabrieltrouve5@gmail.com", username="gabigab117", first_name="Trouvé",
                                          last_name="Gabriel", password="12345678")
