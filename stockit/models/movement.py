from django.db import models
from .abstract import AssociatedItem


class Movement(models.Model):
    char_type = models.CharField(max_length=50, verbose_name="Intitulé", help_text="Type de régularisation")

    class Meta:
        verbose_name = "Régularisation"

    def __str__(self):
        return f"{self.char_type}"


class ProductMovement(AssociatedItem):
    movement = models.ForeignKey(to="Movement", on_delete=models.PROTECT, verbose_name="Mouvement")
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Régularisation produit"
        verbose_name_plural = "Régularisations produits"

    def __str__(self):
        return f"{self.product} - {self.movement} - {self.quantity}"
