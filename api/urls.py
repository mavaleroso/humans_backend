from django.urls import path, include

urlpatterns = [
    path('', include('api.login.urls')),
    path('', include('api.users.urls')),
]