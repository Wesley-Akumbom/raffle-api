from django.urls import path
from .views import TicketHoldersListView

urlpatterns = [
    path('list/', TicketHoldersListView.as_view(), name='purchase'),
]