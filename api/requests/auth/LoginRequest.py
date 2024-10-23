import os
import requests
from api.annotations.auth.postLogin import LoginSerializer
from django.http import JsonResponse

class LoginRequest:

    @staticmethod
    def execute(request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                portal_api_login = os.getenv('PORTAL_API_LOGIN')
                response = requests.post(portal_api_login, data={
                    'username': username,
                    'password': password
                })

                if response.status_code == 200:

                    # return JsonResponse({
                    #     'status_code': response.status_code,
                    #     'status': 'success',
                    #     'data': response.json()
                    # }, status=response.status_code)
                    # breakpoint()
                    return 1
                    
                else:
                    return JsonResponse({
                        'status_code': response.status_code,
                        'status': 'error',
                        'message': 'Invalid username or password'
                    })

            except requests.exceptions.RequestException as e:
                return JsonResponse({
                    'status_code': 500,
                    'status': 'error',
                    'message': f'Error connecting to external API: {str(e)}'
                })        
        return JsonResponse({
            'status_code': 405,
            'status': 'error',
            'message': 'Only POST requests are allowed'
        })