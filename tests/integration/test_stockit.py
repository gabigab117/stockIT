import pytest
from pytest_django.asserts import assertRedirects
from django.test import Client
from django.urls import reverse

from stockit.models import Company, Product, Supplier


@pytest.mark.django_db
def test_create_product_and_supplier_view(client: Client, user_1, company_1: Company):
    # Given an user with a "company" in session
    client.force_login(user_1)
    session = client.session
    session["company"] = company_1.pk
    session.save()
    # When submit create supplier form
    client.post(reverse("stockit:create-supplier"), data={"company": company_1, "name": "ms", "phone": "0344805114",
                                                          "website": "http://ms.fr/", "email": "m@m.com"})
    # Then a supplier is created
    supplier = Supplier.objects.get(name="ms")
    assert supplier.name == "ms"

    # Given an user with a "company" in session
    # When submit create product form
    data_product = {"name": "my product", "ean": "3714567891453", "package": 6, "selling_price": 1,
                    "purchase_price": 0.5, "VAT": "5.5", "suppliers": [supplier.pk], "quantity": 1, "unit": "liter"}
    client.post(reverse("stockit:create-article"), data=data_product)
    # Then a product is created
    product = Product.objects.get(name="my product")
    assert product.name == "my product"


@pytest.mark.django_db
def test_is_redirected_to_select_company_when_user_go_to_create_supplier(client: Client, user_1):
    # Given an user with no "company in session
    client.force_login(user_1)
    # When user wants to go in create-supplier
    r = client.get(reverse("stockit:create-supplier"))
    # The user is redirected to select-company
    assertRedirects(r, f"{reverse('account:select-company')}")


@pytest.mark.django_db
def test_is_redirected_to_select_company_when_user_go_to_create_product(client: Client, user_1):
    # Given an user with no "company in session
    client.force_login(user_1)
    # When user wants to go in create-supplier
    r = client.get(reverse("stockit:create-article"))
    # The user is redirected to select-company
    assertRedirects(r, f"{reverse('account:select-company')}")


@pytest.mark.django_db
def test_products_view(client: Client, user_1, company_1: Company, product_1):
    # Given an user with a "company" in session
    client.force_login(user_1)
    session = client.session
    session["company"] = company_1.pk
    session.save()
    # When user wants to go in product_view
    r = client.get(reverse("stockit:product", kwargs={"pk": product_1.pk, "slug": product_1.slug}))
    # Then, user view the product
    assert r.status_code == 200
    # Then, name of the product is in the template
    assert product_1.name in str(r.content)


@pytest.mark.django_db
def test_get_product_update_view(client: Client, user_1, company_1: Company, product_1):
    # Given an user with a "company" in session
    client.force_login(user_1)
    session = client.session
    session["company"] = company_1.pk
    session.save()
    # When user wants to go in product_update_view
    r = client.get(reverse("stockit:update-product", kwargs={"pk": product_1.pk, "slug": product_1.slug}))
    # Then, user view the product
    assert r.status_code == 200
    # Then, name of the product is in the template
    assert product_1.name in str(r.content)


# test_post_product_update_view
@pytest.mark.django_db
def test_post_product_update_view(client: Client, user_1, company_1: Company, product_1: Product, supplier_1):
    # Given an user with a "company" in session
    client.force_login(user_1)
    session = client.session
    session["company"] = company_1.pk
    session.save()
    # When user wants to update a product
    data = {"name": "new name", "package": 6, "selling_price": 1, "purchase_price": 0.5, "VAT": "5.5",
            "suppliers": [supplier_1.pk], "quantity": 1, "unit": "liter"}
    r = client.post(reverse("stockit:update-product", kwargs={"pk": product_1.pk, "slug": product_1.slug}), data=data)
    # Then, user is redirected to product_view
    assertRedirects(r, reverse("stockit:product", kwargs={"pk": product_1.pk, "slug": product_1.slug}))
    # Then, the product is updated
    product_1.refresh_from_db()
    assert product_1.name == "new name"


@pytest.mark.django_db
def test_create_receipt_view(client: Client, user_1, company_1: Company):
    # Given an user with a "company" in session
    client.force_login(user_1)
    session = client.session
    session["company"] = company_1.pk
    session.save()
    # When user wants to go in create-receipt
    r = client.get(reverse("stockit:create-receipt"))
    # Then, user view the create-receipt
    assert r.status_code == 200
    # Then, the company is in the template
    assert company_1.name in str(r.content)


@pytest.mark.django_db
def test_create_receipt_view_post_product_not_ref_by_supplier(client: Client, user_1, company_1, product_1, supplier_1):
    # Given an user with a "company" in session
    client.force_login(user_1)
    session = client.session
    session["company"] = company_1.pk
    session.save()
    # When user wants to create a receipt with a product not referenced by the supplier
    data = {"date": "2021-09-01", "supplier": [supplier_1.pk], "product_1": product_1.pk, "quantity_1": 6,
            "purchase_price_1": 1.21}
    r = client.post(reverse("stockit:create-receipt"), data=data)
    # Then, the form is not valid
    assert r.context["form"].errors == {"product_1": ["Le produit n'est pas référencé chez le fournisseur"]}


@pytest.mark.django_db
def test_create_receipt_view_post(client: Client, user_1, company_1, product_1: Product, supplier_1, presentation):
    # Given an user with a "company" in session
    client.force_login(user_1)
    session = client.session
    session["company"] = company_1.pk
    session.save()
    product_1.suppliers.add(supplier_1)
    # When user wants to create a receipt
    data = {"date": "2021-09-01", "supplier": [supplier_1.pk], "product_1": product_1.pk, "quantity_1": 6,
            "purchase_price_1": 1.21}
    r = client.post(reverse("stockit:create-receipt"), data=data)
    # Then user is redirected to index
    assertRedirects(r, reverse("index"))
    # Then the product is updated
    product_1.refresh_from_db()
    assert product_1.stock == 6
    # Then the product purchase price is updated
    assert product_1.purchase_price == 1.21
    # Then there is a receipt in the database
    assert company_1.receipt_set.count() == 1
