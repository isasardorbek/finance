from django.contrib import admin
from django.urls import path, include
from transactions.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('', include('transactions.urls')),
]
