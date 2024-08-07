from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_POST

from .forms import SignUpForm, CompanyForm, SelectCompanyForm
from .utils import company_form_validation
from .verification import email_verification_token
from .tasks import send_email_verification


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            try:
                send_email_verification.delay(user_pk=user.pk)
                messages.add_message(request, messages.INFO,
                                     message="Bienvenu(e) sur Stock!t. Merci de confirmer votre email")
                return redirect("index")
            except SMTPException:
                messages.add_message(request, messages.INFO,
                                     message="Une erreur est survenue, merci de nous contacter à test@test.com")
                return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "account/signup.html", context={"form": form})


def activate(request, uidb64, token):
    """
        Activates a user account.

        This function is responsible for handling the account activation process. It decodes the user ID from base64 and
        retrieves the corresponding user object. If the user exists and the provided token is valid, the user's account
        is activated. It displays a success message upon successful activation or an error message if the activation fails.

        Args:
            request: The HTTP request object.
            uidb64: A base64-encoded string representing the user's ID.
            token: A token for verifying the user's email address.

        Returns:
            HttpResponse: Redirects to the landing page after attempting to activate the account, with a success or error message.
        """
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, "Pour continuer, merci de rattacher une entreprise")
        return redirect("index")
    else:
        messages.add_message(request, messages.INFO,
                             "Fail !")
        return redirect("index")


@login_required
def add_company_view(request):
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company_form_validation(request, form)
            messages.add_message(request, messages.INFO, message="Entreprise créée !")
            return redirect("index")
    else:
        form = CompanyForm()
    return render(request, "account/add_company.html", context={"form": form})


class UserLoginView(LoginView):
    template_name = "account/login.html"
    next_page = reverse_lazy("index")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def select_company_view(request):
    user = request.user
    if request.method == "POST":
        form = SelectCompanyForm(user, request.POST)
        if form.is_valid():
            company = form.cleaned_data["company"]
            request.session["company"] = company.pk
            messages.add_message(request, messages.INFO, f"Choix {company} validé.")
            return redirect(request.path)
    else:
        form = SelectCompanyForm(user)
    return render(request, "account/select_company.html", context={"form": form})

