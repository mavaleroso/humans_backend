import os
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.utils import timezone
import requests

class NewlyHiredListService():
    def execute(params):
        return params