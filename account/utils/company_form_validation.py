from account.models import CompanyAddress
from django.db import transaction
from .company_permission import add_company_admin_permission


@transaction.atomic
def company_form_validation(request, form):
    user = request.user
    company = form.save()
    company.users.add(user)
    company_address = CompanyAddress.objects.create(company=company, address_1=form.cleaned_data["address_1"],
                                                    address_2=form.cleaned_data["address_2"] or "nc",
                                                    city=form.cleaned_data["city"],
                                                    zip_code=form.cleaned_data["zip_code"],
                                                    country=form.cleaned_data["country"])
    add_company_admin_permission(user)
    return company, company_address
