import pytest
from account.models import CustomUser, Company
from landing.models import CompanyPresentation


@pytest.fixture
def presentation():
    return CompanyPresentation.objects.create(title="presentation", text="super texte !")


@pytest.fixture
def user_1():
    return CustomUser.objects.create_user(email="gabrieltrouve5@gmail.com", username="gabigab117", first_name="Trouvé",
                                          last_name="Gabriel", password="12345678")


@pytest.fixture
def company_1():
    return Company.objects.create(name='pygabdev', phone="0144865112", email="gab@gabo.com")


@pytest.fixture
def company_2():
    return Company.objects.create(name='pyeldev', phone="0144865113", email="ely@ely.com")
