from django.db import models
from .abstract import StockManagementBase, AssociatedItem


class Invoice(StockManagementBase):
    class Meta:
        ordering = ["identification"]
        verbose_name = "Facture"

    def __str__(self):
        return f"{self.company} - {self.date} - {self.identification}"

    def save(self, *args, **kwargs):
        last_invoice = Invoice.objects.filter(company=self.company).last()
        self.identification = (last_invoice.identification + 1) if last_invoice else 1
        super().save(*args, **kwargs)


class Sales(AssociatedItem):
    invoice = models.ForeignKey(to="Invoice", on_delete=models.PROTECT, verbose_name="Facture")

    class Meta:
        verbose_name = "Vente"
        ordering = ["invoice__identification"]

    def __str__(self):
        return f"{self.invoice} - {self.product.name} {self.quantity}"
