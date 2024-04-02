from django.db import models
from .abstract import StockManagementBase, AssociatedItem


class Inventory(StockManagementBase):
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


class ProductInventory(AssociatedItem):
    inventory = models.ForeignKey(to="Inventory", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Produit inventorié"
        verbose_name_plural = "Produits inventoriés"

    def __str__(self):
        return f"{self.product} {self.quantity} - {self.quantity}"
