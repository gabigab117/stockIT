from account.models import Company
from project.utils import get_pk_from_session


def add_session_company_to_context(request):
    try:
        return {"company_session": Company.objects.get(pk=get_pk_from_session(request.session.get("company")))}
    except AttributeError:
        return {"company_session": None}
