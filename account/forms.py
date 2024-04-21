from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from iso3166 import countries

from account.models import Company


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "last_name", "first_name"]


class CompanyForm(forms.ModelForm):
    address_1 = forms.CharField(max_length=200, label="Adresse")
    address_2 = forms.CharField(max_length=200, label="Complément", required=False)
    city = forms.CharField(max_length=200, label="Ville")
    zip_code = forms.CharField(max_length=5, label="Code postal")
    country = forms.ChoiceField(label="Pays", choices=((c.alpha2.lower(), c.name) for c in countries))

    class Meta:
        model = Company
        exclude = ["users", "identification", "slug"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")


class SelectCompanyForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'] = forms.ModelChoiceField(queryset=Company.objects.filter(users=user), label="Entreprise")
