from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup_view, name="signup"),
    path("booking", views.booking_view, name="flight_booking"),
    path("booking", views.booking_view, name="pod_booking"),
    path("select_base", views.select_base, name="select_base"),
    path("select_date", views.select_date, name="select_date"),
    path("flight_list", views.flight_list, name="flight_list"),
    path("payment_page", views.payment_page, name="payment_page"),
    path("process_payment", views.process_payment, name="process_payment")
]
