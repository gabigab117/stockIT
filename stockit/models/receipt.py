from django.db import models
from .abstract import StockManagementBase, AssociatedItem


class Receipt(StockManagementBase):
    class Meta:
        ordering = ["identification"]
        verbose_name = "Entrée"

    def __str__(self):
        return f"{self.date} - {self.identification} -  {self.company}"

    def save(self, *args, **kwargs):
        last_receipt = Receipt.objects.filter(company=self.company).last()
        self.identification = (last_receipt.identification + 1) if last_receipt else 1
        super().save(*args, **kwargs)


class ProductReceipt(AssociatedItem):
    receipt = models.ForeignKey(to="Receipt", on_delete=models.CASCADE, verbose_name="Entrée")
    purchase_price = models.FloatField(verbose_name="Prix d'achat")

    def __str__(self):
        return f"{self.product}- {self.receipt} - {self.quantity}"

    class Meta:
        verbose_name = "Produit entré"
        verbose_name_plural = "Produits entrés"
