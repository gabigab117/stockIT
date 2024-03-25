from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


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
    company = models.CharField(max_length=200, verbose_name="Entreprise")

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    objects = CustomUserManager()


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom")
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Administrateur")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Utilisateurs")
    # phone
    # website
    # email
    # siret
    # logo
    # address
