from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from account.models import Company
from stockit.models import Product, Supplier


def product_form_layout(include_ean: bool):
    layout = [
        Row(
            Column('name', css_class='form-group col-md-4 mb-0'),
            Column('VAT', css_class='form-group col-md-4 mb-0'),
            Column("state", css_class='form-group col-md-4 mb-0'),
            css_class="form-row"
        ),

        Row(
            Column('purchase_price', css_class='form-group col-md-4 mb-0'),
            Column('selling_price', css_class='form-group col-md-4 mb-0'),
            Column('package', css_class='form-group col-md-4 mb-0'),
            css_class="form-row"
        ),
        Row(
            Column('quantity', css_class='form-group col-md-3 mb-0'),
            Column('unit', css_class='form-group col-md-3 mb-0'),
            css_class="form-row"
        ),
        'suppliers',
        Submit("submit", "Valider")
    ]
    if include_ean:
        layout.insert(1, Row(
            Column("ean", css_class="form-group col-md-3"), css_class="form-row justify-content-center"
        ))
    return Layout(*layout)


class ProductForm(forms.ModelForm):
    ean = forms.CharField()

    class Meta:
        model = Product
        exclude = ["slug", "company", "stock"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["suppliers"] = forms.ModelMultipleChoiceField(
            queryset=Supplier.objects.filter(company=Company.objects.get(pk=request.session["company"])),
            label="Fournisseurs")
        self.helper = FormHelper()
        self.helper.layout = product_form_layout(include_ean=True)


class ProductUpdateForm(ProductForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields.pop("ean")
        self.helper.layout = product_form_layout(include_ean=False)


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ["identification", "company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class='form-group col-md-6 mb-0'),
                Column("phone", css_class='form-group col-md-6 mb-0')
            ),
            Row(
                Column("website", css_class='form-group col-md-6 mb-0'),
                Column("email", css_class='form-group col-md-6 mb-0')
            ),
            Row(
                Column("rib", css_class='form-group col-md-6 mb-0'),
                Column("kbis", css_class='form-group col-md-6 mb-0')
            ),
            Submit("submit", "Valider")
        )


class ReceiptForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)

    def __init__(self, company: Company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["supplier"] = forms.ModelChoiceField(queryset=Supplier.objects.filter(company=company),
                                                         label="Fournisseur")
        self.fields["product_1"] = forms.ModelChoiceField(
            queryset=Product.objects.filter(company=company), label="Produit 1")

        self.fields["quantity_1"] = forms.FloatField(label="Quantité 1")
        self.fields["purchase_price_1"] = forms.FloatField(label="Prix d'achat 1")

        self.add_product_fields(company)

    def add_product_fields(self, company):
        for i in range(2, settings.PRODUCTS_RECEIPT):
            self.fields[f"product_{i}"] = forms.ModelChoiceField(
                queryset=Product.objects.filter(company=company), required=False)

            self.fields[f"quantity_{i}"] = forms.FloatField(label=f"Quantité {i}", required=False)
            self.fields[f"purchase_price_{i}"] = forms.FloatField(label=f"Prix d'achat {i}", required=False)

    def clean(self):
        cleaned_data = super().clean()
        supplier: Supplier = cleaned_data.get("supplier")

        for i in range(1, settings.PRODUCTS_RECEIPT):
            product: Product = cleaned_data.get(f"product_{i}")
            if product:
                if supplier not in product.suppliers.all():
                    self.add_error(f"product_{i}", "Le produit n'est pas référencé chez le fournisseur")
