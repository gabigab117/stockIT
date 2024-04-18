import pytest
from django.test import Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import CustomUser, Company, CompanyAddress
from account.verification import email_verification_token


@pytest.mark.django_db
def test_signup_post_with_activation(client: Client, mailoutbox):
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
    client.get(url)
    user.refresh_from_db()
    # Then his account is active
    assert user.is_active


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
