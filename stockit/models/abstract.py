from django.db import models
from account.models import Company


class StockManagementBase(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name="Utilisateur")
    date = models.DateField()
    identification = models.IntegerField(unique=True)

    class Meta:
        abstract = True


class AssociatedItem(models.Model):
    product = models.ForeignKey(to="Product", on_delete=models.PROTECT, verbose_name="Produit")
    quantity = models.FloatField(verbose_name="Quantité")

    class Meta:
        abstract = True
