from django.contrib.auth.decorators import login_required

from account.models import Company
from .forms import ProductForm, SupplierForm
from .utils import company_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from stockit.models import Product, Supplier


@method_decorator(login_required, name="dispatch")
@method_decorator(company_required, name="dispatch")
class CreateArticle(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("stockit:products")
    template_name = "stockit/create-product.html"

    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=self.request.session["company"])
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


@method_decorator(login_required, name="dispatch")
@method_decorator(company_required, name="dispatch")
class CreateSupplier(CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = reverse_lazy("index")
    template_name = "stockit/create-supplier.html"

    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=self.request.session["company"])
        return super().form_valid(form)


@login_required
@company_required
def products_view(request):
    products_counter = Product.objects.none().count()
    return render(request, "stockit/products.html", context={"products_counter": products_counter})


@login_required
@company_required
def search_products_view(request):
    company = request.session["company"]
    query = request.GET.get("products")
    products = Product.objects.filter(name__icontains=query, company=company) if query else Product.objects.none()
    return render(request, "stockit/products_results.html",
                  context={"products": products, "products_counter": products.count()})
