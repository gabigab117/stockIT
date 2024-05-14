from django.contrib.auth.decorators import login_required

from account.models import Company
from .forms import ProductForm, SupplierForm, ProductUpdateForm
from .utils import company_required, user_is_associated_with_company_product
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db import transaction

from stockit.models import Product, Supplier, Barcode


@method_decorator(login_required, name="dispatch")
@method_decorator(company_required, name="dispatch")
class CreateArticle(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("stockit:products")
    template_name = "stockit/create-product.html"

    @transaction.atomic
    def form_valid(self, form):
        form.instance.company = Company.objects.get(pk=self.request.session["company"])
        result = super().form_valid(form)
        Barcode.objects.create(ean=form.cleaned_data["ean"], main=True, product=form.instance)
        return result

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


@login_required
@company_required
@user_is_associated_with_company_product
def product_view(request, pk, slug):
    product: Product = get_object_or_404(Product, pk=pk)
    return render(request, "stockit/product.html", context={"product": product})


@login_required
@company_required
@user_is_associated_with_company_product
def product_update_view(request, pk, slug):
    product: Product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form: ProductUpdateForm = ProductUpdateForm(data=request.POST, instance=product, request=request)
        if form.is_valid():
            form.save()
            return redirect(product)
    else:
        form: ProductUpdateForm = ProductUpdateForm(instance=product, request=request)
    return render(request, "stockit/update-product.html", context={"form": form})
