from django.urls import path
from .views import CreateArticle, CreateSupplier, products_view, search_products_view


app_name = "stockit"
urlpatterns = [
    path("create-article", CreateArticle.as_view(), name="create-article"),
    path("create-supplier", CreateSupplier.as_view(), name="create-supplier"),
    path("products-list/", products_view, name="products"),
    path("products/results/", search_products_view, name="search-products")
]
