from django.contrib.auth.decorators import login_required

from account.models import Company
from .forms import ProductForm, SupplierForm
from .utils import company_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from project.utils import get_pk_from_session

from stockit.models import Product, Supplier


@method_decorator(login_required, name="dispatch")
@method_decorator(company_required, name="dispatch")
class CreateArticle(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("index")
    template_name = "stockit/create-product.html"

    def form_valid(self, form):
        form.instance.company = self.request.session["company"]
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(company_required, name="dispatch")
class CreateSupplier(CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy("index")
    template_name = "stockit/create-supplier.html"

    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=get_pk_from_session(self.request.session["company"]))
        return super().form_valid(form)
