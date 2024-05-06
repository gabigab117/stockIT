from django.urls import path
from .views import CreateArticle, CreateSupplier


app_name = "stockit"
urlpatterns = [
    path("create-article", CreateArticle.as_view(), name="create-article"),
    path("create-supplier", CreateSupplier.as_view(), name="create-supplier"),
]
