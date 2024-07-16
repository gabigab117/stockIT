from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from ninja import Router
from ninja.security import django_auth, django_auth_superuser

from .schemas import RegisterSchema, LoginSchema
from .tasks import send_email_verification
from .verification import email_verification_token

account_api = Router()

User = get_user_model()


@account_api.post("/register", url_name="register")
def register(request, payload: RegisterSchema):
    if payload.password != payload.password2:
        return {"Erreur": "Les mots de passe ne correspondent pas."}
    user = User.objects.create_user(username=payload.username, email=payload.email, password=payload.password,
                                    last_name=payload.last_name, first_name=payload.first_name)
    user.is_active = False
    user.save()
    current_site = get_current_site(request)
    send_email_verification.apply_async(args=[user.pk, current_site.domain], kwargs={'api': True})
    return {"username": f"{user.username} a bien été créé !"}


@account_api.get("/activate/{uidb64}/{token}", url_name="activate")
def activate(request, uidb64: str, token: str):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        return {"message": "Compte activé !"}
    return {"message": "Erreur d'activation."}


@account_api.post("/login", url_name="login")
def login_api(request, payload: LoginSchema):
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None:
        login(request, user)
        return {"message": "Login OK"}
    return {"message": "Erreur de login"}


@account_api.post("/logout", url_name="logout")
def logout_api(request):
    logout(request)
    return {"message": "Logout OK"}


@account_api.get("/is_logged_in", url_name="is_logged_in", auth=django_auth)
def is_logged_in(request):
    return {"is_logged_in": request.user.is_authenticated}
