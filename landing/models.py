from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class CompanyPresentation(models.Model):
    title = models.CharField(max_length=100)
    text = CKEditor5Field(config_name="extends")
