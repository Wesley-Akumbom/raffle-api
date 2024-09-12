from django.urls import path
from .views import (
    RaffleCreateView, RaffleListView, RaffleDetailView,
    RaffleUpdateView, RaffleDeleteView
)

urlpatterns = [
    path('list', RaffleListView.as_view(), name='raffle-list'),
    path('create/', RaffleCreateView.as_view(), name='raffle-create'),
    path('<int:id>', RaffleDetailView.as_view(), name='raffle-detail'),
    path('update/<int:id>/', RaffleUpdateView.as_view(), name='raffle-update'),
    path('delete/<int:id>', RaffleDeleteView.as_view(), name='raffle-delete'),
]
