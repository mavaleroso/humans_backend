import os
import requests
from rest_framework import serializers

# Define the LoginSerializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True)

class NewlyHiredListRequest:

    @staticmethod
    def execute(request, page=1, items_per_page=10):
        api_key = os.getenv('IRIS_API_TOKEN')
        iris_api_newly_hired = os.getenv('IRIS_URL') + f'/api/hired-applicants/?page={page}'

        request_data = request.GET.copy()
        request_data['format'] = 'datatables'

        response_newly_hired_list = requests.get(url=iris_api_newly_hired, params=request_data, headers={
            'Authorization': f'Token {api_key}',
        })

        if response_newly_hired_list.status_code == 200:
            return response_newly_hired_list.json()
        else:
            return {
                'status_code': 422,
                'status': 'error',
                'message': 'API Error'
            }
