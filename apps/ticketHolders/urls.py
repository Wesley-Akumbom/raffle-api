from django.urls import path
from .views import TicketHoldersListView, TicketHoldersDetailView

urlpatterns = [
    path('list/', TicketHoldersListView.as_view(), name='list-tickets'),
    path('<int:user_id>', TicketHoldersDetailView.as_view(), name='view-ticket'),
]