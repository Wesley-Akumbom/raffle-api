from django.urls import path
from .views import PaymentView, CheckPaymentStatusView, MoMoCallbackView

urlpatterns = [
    path('purchase/', PaymentView.as_view(), name='purchase'),
    path('status/<str:transaction_id>/', CheckPaymentStatusView.as_view(), name='check_payment_status'),
    path('momo-callback/', MoMoCallbackView.as_view(), name='momo_callback'),
]