from django.urls import path
from .views import CheckActiveSessionView

urlpatterns = [
    path('verify_token', CheckActiveSessionView.as_view(), name='session'),
]