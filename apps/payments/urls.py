from django.urls import path
from .views import PaymentView, PaymentWebhookView

urlpatterns = [
    path('purchase/', PaymentView.as_view(), name='purchase'),
    path('stripe-webhooks/', PaymentWebhookView.as_view(), name='stripe-webhooks'),
]