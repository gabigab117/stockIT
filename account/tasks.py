from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model

from account.verification.token_generator import email_verification_token

User = get_user_model()


@shared_task
def send_email_verification(user_pk, domain, api=False):
    user = User.objects.get(pk=user_pk)
    subject = 'Account activation'
    template = 'email/api_verification.html' if api else 'email/verification.html'
    body = render_to_string(
        template_name=template,
        context=
        {
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': email_verification_token.make_token(user),
        }
    )
    EmailMessage(to=[user.email], subject=subject, body=body).send()
