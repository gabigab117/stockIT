import pytest
from pytest_django.asserts import assertRedirects
from django.test import Client, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import CustomUser, Company
from account.verification import email_verification_token


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_signup_post_with_activation(client: Client, mailoutbox, presentation):
    # Given a user wants to create an account
    data = {"email": "test@test.com", "username": "test", "last_name": "Trouvé", "first_name": "Patrick",
            "password1": "Roger_12345678", "password2": "Roger_12345678"}
    client.post(reverse("account:signup"), data=data)
    # print(response.context['form'].errors)
    user = CustomUser.objects.get(email="test@test.com")
    # When user submits the form,
    # Then his account is not active and an email is sent
    assert user.is_active is False
    assert len(mailoutbox) == 1

    # When user wants to activate his account
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    url = reverse("account:activate", kwargs={"uidb64": uidb64, "token": token})
    r = client.get(url)
    user.refresh_from_db()
    # Then his account is active
    assert user.is_active
    assertRedirects(r, reverse("index"), 302)


@pytest.mark.django_db
def test_add_company_view(client: Client, user_1):
    # Given user who add a company
    client.force_login(user_1)
    # When user submits the form,
    data = {"address_1": "adresse", "city": "Ons en Bray", "zip_code": "60650", "country": "fr",
            "name": "py", "phone": "0344785145", "email": "t@t.com", "website": "www.g.com"}
    client.post(reverse("account:add-company"), data)
    company = Company.objects.get(name="py")
    # Then a company with address is created, and user has admin status perm
    assert company.companyaddress.city == "Ons en Bray"
    assert user_1.has_perm("account.company_admin_status")


@pytest.mark.django_db
def test_select_company_view(client: Client, user_1, company_1: Company, company_2):
    # Given user who select a company
    company_1.users.add(user_1)
    client.force_login(user_1)
    r = client.get(reverse("account:select-company"))
    # in the list of choices there are only the companies of which the user is a part
    assert "pygabdev" in str(r.content)
    assert "pyeldev" not in str(r.content)
    # When user submits the form
    r = client.post(reverse("account:select-company"), data={"company": company_1.id})
    # Then the session has a key "company" with the name and id of company instance
    assert client.session["company"] == company_1.pk
    assertRedirects(r, reverse("account:select-company"), 302)
