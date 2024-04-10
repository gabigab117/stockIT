from django.urls import path
from .views import signup_view, activate


app_name = "account"
urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("activate/<str:uidb64>/<str:token>", activate, name="activate")
]
