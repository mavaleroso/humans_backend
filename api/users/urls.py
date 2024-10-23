from django.urls import path
from .views import CheckActiveSessionView

urlpatterns = [
    path('session/', CheckActiveSessionView.as_view(), name='session'),
]