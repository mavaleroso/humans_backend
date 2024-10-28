from django.urls import path
from .views import CheckActiveSessionView

urlpatterns = [
    path('rsp/newly_hired_list', CheckActiveSessionView.as_view(), name='session'),
]