import os
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.utils import timezone
import requests
from api.dataModels.CustomUsers import CustomUser

User = get_user_model() 

class LoginService():
    def execute(params):
        data = params['data']
        api_key = data['key']
        portal_api_employee_details = os.getenv('PORTAL_API_EMPLOYEE_DETAILS')
        username = data['username']
        try:
            user = User.objects.get(username=username)
            user.last_login = timezone.now()
            user.save()
        except User.DoesNotExist:
            response_employee_details = requests.get(f"{portal_api_employee_details}{username}", headers={
                'Authorization': f"Token {api_key}"
            })
            api_response_employee_details_data = response_employee_details.json()
            employee_details_data = api_response_employee_details_data[0]
            CustomUser.objects.create(
                employee_id=employee_details_data['employee_id'],
                id_number=employee_details_data['id_number'],
                last_login=timezone.now(),
                username=employee_details_data['username'],
                first_name=employee_details_data['first_name'],
                middle_name=employee_details_data['middle_name'],
                last_name=employee_details_data['last_name'],
                contact=employee_details_data['contact'],
                account_number=employee_details_data['account_number'],
                position=employee_details_data['position'],
                division=employee_details_data['division'],
                section=employee_details_data['section'],
                area_of_assignment=employee_details_data['area_of_assignment'],
                gender=employee_details_data['gender'],
                birthdate=employee_details_data['birthdate'],
                image_path=employee_details_data['image_path'],
                status=employee_details_data['status'],
            )

        token, created = Token.objects.get_or_create(user=user)
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'image_path': user.image_path,
            'position': user.position,
            'division': user.division,
            'section': user.section,
            'api_token': token.key,

        }
        return user_data