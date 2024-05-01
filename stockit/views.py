from django.contrib.auth.decorators import login_required

from .forms import ProductForm
from .utils import company_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from stockit.models import Product


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
