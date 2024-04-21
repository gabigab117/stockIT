from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify

from iso3166 import countries


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, last_name, first_name, password, **kwargs):
        if not email:
            raise ValueError("Un email doit être renseigné")
        if not username:
            raise ValueError("Username manquant")
        if not last_name:
            raise ValueError("Nom manquant")
        if not first_name:
            raise ValueError("Prénom manquant")

        user = self.model(username=username, email=self.normalize_email(email), last_name=last_name,
                          first_name=first_name, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, last_name, first_name, password, **kwargs):
        user = self.create_user(email, username, last_name, first_name, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    objects = CustomUserManager()


class UserAddress(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    address_1 = models.CharField(max_length=1024, help_text="Voirie, numéro de rue", verbose_name="Adresse 1")
    address_2 = models.CharField(max_length=1024, help_text="Bât, étage, lieu-dit", verbose_name="Adresse 2",
                                 blank=True)
    city = models.CharField(max_length=1024, verbose_name="Commune")
    zip_code = models.CharField(max_length=32, verbose_name="Code Postal")
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in countries])

    def __str__(self):
        return f"{self.user} - {self.city}"


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom", unique=True, help_text="Raison sociale")
    slug = models.SlugField(blank=True)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="Utilisateurs",
                                   related_name="companies", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    website = models.URLField(verbose_name="Site internet", blank=True)
    email = models.EmailField()
    kbis = models.FileField(null=True, blank=True)
    identification = models.IntegerField(unique=True, blank=True)

    class Meta:
        verbose_name = "Entreprise"
        permissions = [
            ("company_admin_status", "User has all the rights on company"),
        ]

    @property
    def identification_name(self):
        # Je pourrais faire un split sur _ puis associer le slug et le pk après
        return f"{self.slug}_{self.pk}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        last_company = Company.objects.last()
        self.identification = (last_company.identification + 1) if last_company else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.identification}"


class CompanyAddress(models.Model):
    company = models.OneToOneField(to=Company, on_delete=models.CASCADE, verbose_name="Entreprise")
    address_1 = models.CharField(max_length=1024, help_text="Voirie, numéro de rue", verbose_name="Adresse 1")
    address_2 = models.CharField(max_length=1024, help_text="Bât, étage, lieu-dit", verbose_name="Adresse 2",
                                 blank=True)
    city = models.CharField(max_length=1024, verbose_name="Commune")
    zip_code = models.CharField(max_length=32, verbose_name="Code Postal")
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in countries])

    def __str__(self):
        return f"{self.company} - {self.city}"

    class Meta:
        verbose_name = "Address"
