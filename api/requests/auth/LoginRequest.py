import os
import requests
from api.annotations.auth.postLogin import LoginSerializer

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
                    results =  response.json()

                   
                    api_key = results['key']
                    portal_api_employee_details = os.getenv('PORTAL_API_EMPLOYEE_DETAILS')
                    response_employee_details = requests.get(f"{portal_api_employee_details}{username}", headers={
                        'Authorization': f"Token {api_key}"
                    })

                    if response_employee_details.status_code == 200:
                        return {
                            'status_code': response.status_code,
                            'status': 'success',
                            'data': {
                                'key': results['key'],
                                'username': username,
                                'password': password
                            }
                        }
                    else :
                        return {
                           'status_code': 422,
                            'status': 'error',
                            'message': 'No user found in portal'
                        }
                    
                else:
                    return {
                        'status_code': response.status_code,
                        'status': 'error',
                        'message': 'Invalid username or password'
                    }

            except requests.exceptions.RequestException as e:
                return {
                    'status_code': 500,
                    'status': 'error',
                    'message': f'Error connecting to external API: {str(e)}'
                }   
        return {
            'status_code': 405,
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }