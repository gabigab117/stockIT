from django.urls import path
from .views import CreateArticle


app_name = "stockit"
urlpatterns = [
    path("create-article", CreateArticle.as_view(), name="create-article")
]
