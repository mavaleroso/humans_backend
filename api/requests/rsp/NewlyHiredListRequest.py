import os
import requests
from rest_framework import serializers

# Define the LoginSerializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True)

class NewlyHiredListRequest:

    @staticmethod
    def execute(request):
        api_key = os.getenv('IRIS_API_TOKEN')
        iris_api_newly_hired = os.getenv('IRIS_URL')+'/api/hired-applicants/'
        response_newly_hired_list = requests.get(iris_api_newly_hired, headers={
            'Authorization': f"Token {api_key}"
        })

        if response_newly_hired_list.status_code == 200:
             return {
                'status_code': 200,
                'status': 'success',
                'data': response_newly_hired_list.json()
            }
        else:
            return {
                    'status_code': 422,
                    'status': 'error',
                    'message': 'API Error'
                }
