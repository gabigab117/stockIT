from django.contrib import admin

from stockit.models import Supplier, Product, Barcode

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Barcode)
