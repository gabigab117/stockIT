from django.contrib import admin

from stockit.models import Supplier, Product, Barcode, ProductReceipt, Receipt

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Barcode)
admin.site.register(Receipt)
admin.site.register(ProductReceipt)

