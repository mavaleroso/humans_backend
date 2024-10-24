import os
import requests
from rest_framework import serializers

# Define the LoginSerializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True)

class LoginRequest:

    @staticmethod
    def execute(request):
        # Initialize the serializer with the request data
        serializer = LoginSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Extract the validated data
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                # Get the external API URLs from environment variables
                portal_api_login = os.getenv('PORTAL_API_LOGIN')
                portal_api_employee_details = os.getenv('PORTAL_API_EMPLOYEE_DETAILS')

                # Perform login request to external API
                response = requests.post(portal_api_login, data={
                    'username': username,
                    'password': password
                })

                if response.status_code == 200:
                    results = response.json()
                    api_key = results['key']

                    # Fetch employee details using the token received
                    response_employee_details = requests.get(f"{portal_api_employee_details}{username}", headers={
                        'Authorization': f"Token {api_key}"
                    })

                    if response_employee_details.status_code == 200:
                        # Return successful response with the employee details
                        return {
                            'status_code': 200,
                            'status': 'success',
                            'data': {
                                'key': api_key,
                                'username': username,
                                'employee_details': response_employee_details.json()
                            }
                        }
                    else:
                        # Handle case when no employee details are found
                        return {
                            'status_code': 422,
                            'status': 'error',
                            'message': 'No user found in portal'
                        }

                else:
                    # Handle login failure
                    return {
                        'status_code': response.status_code,
                        'status': 'error',
                        'message': 'Invalid username or password'
                    }

            except requests.exceptions.RequestException as e:
                # Handle errors with external API communication
                return {
                    'status_code': 500,
                    'status': 'error',
                    'message': f'Error connecting to external API: {str(e)}'
                }

        # Handle validation failure from serializer
        return {
            'status_code': 400,
            'status': 'error',
            'message': serializer.errors
        }
