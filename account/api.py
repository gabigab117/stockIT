from django.contrib.auth import get_user_model
from ninja import Router

from .schemas import RegisterSchema
from .tasks import send_email_verification

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
    send_email_verification.delay(user.pk)
    return {"username": f"{user.username} a bien été créé !"}
