from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Product(models.Model):

    class VAT(models.TextChoices):
        REDUCED = "5.5", _("Réduit 5.5%")
        INTERMEDIATE = "10", _("Intermédiaire 10%")
        NORMAL = "20", _("Normal 20%")

    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(blank=True)
    ean = models.CharField(max_length=13)
    package = models.IntegerField(verbose_name="Colis")
    selling_price = models.FloatField(verbose_name="Prix de vente")
    purchase_price = models.FloatField(verbose_name="Prix d'achat")
    VAT = models.CharField(max_length=3, choices=VAT)
    stock = models.FloatField(default=0)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="Utilisateur/Entreprise")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Receipt(models.Model):
    date = models.DateField()
    identification = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        last_receipt = Receipt.objects.last()
        self.identification = (last_receipt.identification + 1) if last_receipt else 1
        super().save(*args, **kwargs)


class ProductReceipt(models.Model):
    receipt = models.ForeignKey(to="Receipt", on_delete=models.CASCADE, verbose_name="Entrée")
    product = models.ForeignKey(to="Product", on_delete=models.PROTECT, verbose_name="Article")
    purchase_price = models.FloatField(verbose_name="Prix d'achat")


class Inventory(models.Model):
    date = models.DateField()
    identification = models.IntegerField(unique=True)

    def save(self, *args, **kwargs):
        last_inventory = Inventory.objects.last()
        self.identification = (last_inventory.identification + 1) if last_inventory else 1
        super().save(*args, **kwargs)


class ProductInventory(models.Model):
    inventory = models.ForeignKey(to="Inventory", on_delete=models.CASCADE)
    product = models.ForeignKey(to="Product", on_delete=models.PROTECT, verbose_name="Article")
    quantity = models.FloatField(verbose_name="Quantité")

# Ventes et régules
