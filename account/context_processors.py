from account.models import Company
from django.core.exceptions import ObjectDoesNotExist


def add_session_company_to_context(request):
    try:
        return {"company_session": Company.objects.get(pk=request.session.get("company"))}
    except ObjectDoesNotExist:
        return {"company_session": None}
