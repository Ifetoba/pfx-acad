from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path("create-checkout-session/<int:course_id>", views.create_checkout_session, name="create-checkout-session"),
    # path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("success/<int:course_id>", views.payment_success, name="payment-success"),
]
