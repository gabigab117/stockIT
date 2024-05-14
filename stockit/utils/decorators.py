from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from stockit.models import Company, Product


def company_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("company"):
            return redirect("account:select-company")
        response = view_func(request, *args, **kwargs)
        return response
    return wrapper


def user_is_associated_with_company_product(view_func):
    def wrapper(request, *args, **kwargs):
        company: Company = Company.objects.get(pk=request.session.get("company"))
        product: Product = Product.objects.get(pk=kwargs["pk"])
        if request.user not in company.users.all() or product.company != company:
            raise PermissionDenied()
        response = view_func(request, *args, **kwargs)
        return response
    return wrapper
