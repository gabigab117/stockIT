def add_session_company_to_context(request):
    return {"company_session": request.session.get("company", None)}
