from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls.auth_urls')),
    path('api/users/', include('apps.users.urls.urls')),
    path('api/raffles/', include('apps.raffles.urls')),
    path('api/tickets/', include('apps.tickets.urls')),
]