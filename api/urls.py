from django.urls import path, include

urlpatterns = [
    path('', include('api.controllers.auth.urls')),
    path('', include('api.controllers.users.urls')),
]