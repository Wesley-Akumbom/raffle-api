from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView,
    TicketDetailView,
    TicketUpdateView,
    TicketDeleteView,
)

urlpatterns = [
    path('list', TicketListView.as_view(), name='ticket-list'),
    path('create/', TicketCreateView.as_view(), name='ticket-create'),
    path('<int:id>', TicketDetailView.as_view(), name='ticket-detail'),
    path('update/<int:id>/', TicketUpdateView.as_view(), name='ticket-update'),
    path('delete/<int:id>', TicketDeleteView.as_view(), name='ticket-delete')
]
