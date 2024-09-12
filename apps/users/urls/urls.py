from django.urls import path
from apps.users.views import (
   UserListView,
   UserDetailView,
   UserUpdateView,
   UserDeleteView,
   UserDeleteAllView
)

urlpatterns = [
    path('list', UserListView.as_view(), name='user_list'),
    path('update/<int:id>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:id>', UserDeleteView.as_view(), name='user_delete'),
    path('delete_all/', UserDeleteAllView.as_view(), name='user_delete_all'),
    path('<int:id>', UserDetailView.as_view(), name='user_detail'),
]