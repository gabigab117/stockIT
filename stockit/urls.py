from django.urls import path
from .views import CreateArticle, CreateSupplier, products_view, search_products_view, product_view, \
    product_update_view, create_receipt_view

app_name = "stockit"
urlpatterns = [
    path("create-article", CreateArticle.as_view(), name="create-article"),
    path("create-supplier", CreateSupplier.as_view(), name="create-supplier"),
    path("products-list/", products_view, name="products"),
    path("products/results/", search_products_view, name="search-products"),
    path("product/<int:pk>/<str:slug>/", product_view, name="product"),
    path("product-update/<int:pk>/<str:slug>/", product_update_view, name="update-product"),
    path("create-receipt/", create_receipt_view, name="create-receipt"),
]
