import pytest

from account.models import Company
from account.utils import add_company_admin_permission


@pytest.mark.django_db
def test_identification_company(company_1):
    # Given two companies created in DB
    # When the second is created
    company = Company.objects.create(name='docdev', phone="0144865113", email="doc@gabo.com")
    # Then identification field must be 2
    assert company.identification == 2


@pytest.mark.django_db
def test_add_company_perm(user_1):
    # Given an use
    # When we call add_company_admin_permission
    add_company_admin_permission(user_1)
    # Then user has admin perm
    assert user_1.has_perm("account.company_admin_status")
