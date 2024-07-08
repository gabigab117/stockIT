from django.conf import settings
from django.db import transaction

from account.models import Company
from stockit.forms import ReceiptForm
from stockit.models import Receipt, Product, ProductReceipt


def receipt_form_validation(form: ReceiptForm, company: Company,  movement: str):
    with transaction.atomic():
        receipt = Receipt.objects.create(date=form.cleaned_data["date"], company=company,
                                         supplier=form.cleaned_data["supplier"], status=Receipt.Status.VALIDATED)

        for i in range(1, settings.PRODUCTS_RECEIPT):
            product: Product = form.cleaned_data[f"product_{i}"]
            quantity = form.cleaned_data[f"quantity_{i}"]
            purchase_price = form.cleaned_data[f"purchase_price_{i}"]
            if product and quantity and purchase_price:
                product_receipt = ProductReceipt.objects.create(receipt=receipt, purchase_price=purchase_price,
                                                                product=product, quantity=quantity)
                product.update_price(product_receipt)
                product.update_quantity(product_receipt, movement)
