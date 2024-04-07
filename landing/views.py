from django.shortcuts import render
from .models import CompanyPresentation


def index_view(request):
    presentation = CompanyPresentation.objects.get(title="presentation")
    return render(request, "landing/index.html", context={"presentation": presentation})
