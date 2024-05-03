from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from account.models import Company


class Supplier(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name="Entreprise/Utilisateur")
    name = models.CharField(max_length=50, verbose_name="Nom")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    website = models.URLField(verbose_name="Site internet")
    email = models.EmailField()
    rib = models.FileField(verbose_name="RIB", blank=True, null=True)
    kbis = models.FileField(verbose_name="KBIS", blank=True, null=True)
    identification = models.IntegerField()

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
    suppliers = models.ManyToManyField(to=Supplier, verbose_name="Fournisseurs")

    class Meta:
        verbose_name = "Produit"

    def __str__(self):
        return f"{self.name} - {self.company}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Promotion(models.Model):
    product = models.ForeignKey(to=Product, verbose_name="Produit", on_delete=models.CASCADE)
    start = models.DateField(verbose_name="Début")
    end = models.DateField(verbose_name="Fin")
    price = models.FloatField(verbose_name="Prix de vente")

    def __str__(self):
        return f"{self.product} - {self.start} - {self.end} - {self.price}"

    def clean(self):
        existing_promotion = Promotion.objects.filter(product=self.product, start__lte=self.end, end__gte=self.start)
        if self.pk:
            existing_promotion = existing_promotion.exclude(pk=self.pk)
        if existing_promotion.exists():
            raise ValidationError(_("Chevauchement interdit"))

    class Meta:
        ordering = ["product__name", "end"]
