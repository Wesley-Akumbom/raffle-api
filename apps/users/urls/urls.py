from django.urls import path
from apps.users.views.views import (
   UserListView,
   UserDetailView,
   UserUpdateView,
   UserDeleteView
)

urlpatterns = [
    path('list', UserListView.as_view(), name='user_list'),
    path('update/<int:id>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:id>', UserDeleteView.as_view(), name='user_delete'),
    path('<int:id>', UserDetailView.as_view(), name='user_detail'),
]