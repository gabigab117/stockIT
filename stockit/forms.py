from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from stockit.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["slug", "company", "stock"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('VAT', css_class='form-group col-md-6 mb-0'),
                css_class="form-row"
            ),
            Row(
                Column("ean", css_class="form-group col-md-3"), css_class="form-row justify-content-center"
            ),
            Row(
                Column('purchase_price', css_class='form-group col-md-4 mb-0'),
                Column('selling_price', css_class='form-group col-md-4 mb-0'),
                Column('package', css_class='form-group col-md-4 mb-0'),
                css_class="form-row"
            ),
            'suppliers',
            Submit("submit", "Valider")
        )