from django.db import models
from .abstract import StockManagementBase, AssociatedItem


class Receipt(StockManagementBase):

    class Status(models.TextChoices):
        CREATED = "created", "Création"
        VALIDATED = "validated", "Validée"
        CANCELLED = "cancelled", "Annulée"

    supplier = models.ForeignKey(to="Supplier", on_delete=models.PROTECT)
    status = models.CharField(max_length=9, choices=Status, verbose_name="Statut")

    class Meta:
        ordering = ["identification"]
        verbose_name = "Entrée"

    def __str__(self):
        return f"{self.date} - {self.identification} -  {self.company} - {self.status}"

    def save(self, *args, **kwargs):
        last_receipt = Receipt.objects.filter(company=self.company).last()
        self.identification = (last_receipt.identification + 1) if last_receipt else 1
        super().save(*args, **kwargs)


class ProductReceipt(AssociatedItem):
    receipt = models.ForeignKey(to="Receipt", on_delete=models.PROTECT, verbose_name="Entrée")
    purchase_price = models.FloatField(verbose_name="Prix d'achat")

    def __str__(self):
        return f"{self.product}- {self.receipt} - {self.quantity}"

    class Meta:
        verbose_name = "Produit entré"
        verbose_name_plural = "Produits entrés"
