from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from account.models import Company


class Supplier(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name="Entreprise/Utilisateur")
    name = models.CharField(max_length=50, verbose_name="Nom")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    website = models.URLField(verbose_name="Site internet")
    email = models.EmailField()
    rib = models.FileField(verbose_name="RIB", blank=True, null=True)
    kbis = models.FileField(verbose_name="KBIS", blank=True, null=True)
    identification = models.IntegerField(unique=True)

    class Meta:
        ordering = ["identification"]
        verbose_name = "Fournisseur"

    def save(self, *args, **kwargs):
        last_supplier = Supplier.objects.filter(company=self.company).last()
        self.identification = (last_supplier.identification + 1) if last_supplier else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.company}"


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
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE,
                                verbose_name="Entreprise")

    class Meta:
        verbose_name = "Produit"

    def __str__(self):
        return f"{self.name} - {self.company}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Receipt(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name="Utilisateur")
    date = models.DateField()
    identification = models.IntegerField(unique=True)

    class Meta:
        ordering = ["identification"]
        verbose_name = "Entrée"

    def __str__(self):
        return f"{self.date} - {self.identification} -  {self.company}"

    def save(self, *args, **kwargs):
        last_receipt = Receipt.objects.filter(company=self.company).last()
        self.identification = (last_receipt.identification + 1) if last_receipt else 1
        super().save(*args, **kwargs)


class ProductReceipt(models.Model):
    receipt = models.ForeignKey(to="Receipt", on_delete=models.CASCADE, verbose_name="Entrée")
    product = models.ForeignKey(to="Product", on_delete=models.PROTECT, verbose_name="Article")
    purchase_price = models.FloatField(verbose_name="Prix d'achat")
    quantity = models.FloatField(verbose_name="Quantité")

    def __str__(self):
        return f"{self.product}- {self.receipt} - {self.quantity}"

    class Meta:
        verbose_name = "Produit entré"
        verbose_name_plural = "Produits entrés"


class Inventory(models.Model):
    company = models.ForeignKey(to=Company, verbose_name="Utilisateur", on_delete=models.CASCADE)
    date = models.DateField()
    identification = models.IntegerField(unique=True)
    closed = models.BooleanField(verbose_name="Fermé", default=False)

    class Meta:
        ordering = ["identification"]
        verbose_name = "Inventaire"

    def __str__(self):
        return f"{self.company} - {self.date}"

    def save(self, *args, **kwargs):
        last_inventory = Inventory.objects.filter(company=self.company).last()
        self.identification = (last_inventory.identification + 1) if last_inventory else 1
        super().save(*args, **kwargs)


class ProductInventory(models.Model):
    inventory = models.ForeignKey(to="Inventory", on_delete=models.CASCADE)
    product = models.ForeignKey(to="Product", on_delete=models.PROTECT, verbose_name="Article")
    quantity = models.FloatField(verbose_name="Quantité")

    class Meta:
        verbose_name = "Produit inventorié"
        verbose_name_plural = "Produits inventoriés"

    def __str__(self):
        return f"{self.product} {self.quantity} - {self.quantity}"


class Movement(models.Model):
    char_type = models.CharField(max_length=50, verbose_name="Intitulé", help_text="Type de régularisation")

    class Meta:
        verbose_name = "Régularisation"

    def __str__(self):
        return f"{self.char_type}"


class ProductMovement(models.Model):
    movement = models.ForeignKey(to="Movement", on_delete=models.PROTECT, verbose_name="Mouvement")
    product = models.ForeignKey(to="Product", on_delete=models.PROTECT, verbose_name="Produit")
    quantity = models.FloatField(verbose_name="Quantité")

    class Meta:
        verbose_name = "Régularisation produit"
        verbose_name_plural = "Régularisations produits"

    def __str__(self):
        return f"{self.product} - {self.movement} - {self.quantity}"


class Invoice(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name="Utilisateur")
    date = models.DateField(auto_now_add=True)
    identification = models.IntegerField(unique=True)

    class Meta:
        ordering = ["identification"]
        verbose_name = "Facture"

    def __str__(self):
        return f"{self.company} - {self.date} - {self.identification}"

    def save(self, *args, **kwargs):
        last_invoice = Invoice.objects.filter(company=self.company).last()
        self.identification = (last_invoice.identification + 1) if last_invoice else 1
        super().save(*args, **kwargs)


class Sales(models.Model):
    invoice = models.ForeignKey(to="Invoice", on_delete=models.PROTECT, verbose_name="Facture")
    product = models.ForeignKey(to="Product", on_delete=models.PROTECT, verbose_name="Produit", related_name="sales")
    quantity = models.FloatField(verbose_name="Quantité")

    class Meta:
        verbose_name = "Vente"
        ordering = ["invoice__identification"]

    def __str__(self):
        return f"{self.invoice} - {self.product.name} {self.quantity}"
