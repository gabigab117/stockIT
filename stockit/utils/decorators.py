from django.shortcuts import redirect


def company_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("company"):
            return redirect("account:select-company")
        response = view_func(request, *args, **kwargs)
        return response
    return wrapper
