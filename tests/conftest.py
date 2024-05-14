import pytest
from account.models import CustomUser, Company
from stockit.models import Supplier, Product, Barcode
from landing.models import CompanyPresentation


@pytest.fixture
def presentation():
    return CompanyPresentation.objects.create(title="presentation", text="super texte !")


@pytest.fixture
def user_1():
    return CustomUser.objects.create_user(email="gabrieltrouve5@gmail.com", username="gabigab117", first_name="Trouvé",
                                          last_name="Gabriel", password="12345678")


@pytest.fixture
def company_1(user_1):
    company = Company.objects.create(name='pygabdev', phone="0144865112", email="gab@gabo.com")
    company.users.add(user_1)
    return company


@pytest.fixture
def company_2():
    return Company.objects.create(name='pyeldev', phone="0144865113", email="ely@ely.com")


@pytest.fixture
def product_1(company_1):
    product = Product.objects.create(name="product_1", company=company_1, quantity=1, unit="liter",
                                     selling_price=1, purchase_price=0.5, package=6, VAT="5.5")
    Barcode.objects.create(ean="1234567890123", main=True, product=product)
    return product


# Create a Supplier
@pytest.fixture
def supplier_1(company_1):
    return Supplier.objects.create(name="supplier_1", company=company_1, phone="0144865114", email="t@t.com",
                                      website="http://t.com")
