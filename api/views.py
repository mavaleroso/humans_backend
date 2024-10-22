from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        # Extract username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # External API endpoint URL
        external_api_url = 'https://caraga-portal.dswd.gov.ph/api/rest-auth/login/'
        
        # Send a POST request to the external API
        try:
            response = requests.post(external_api_url, data={
                'username': username,
                'password': password
            })
            
            # Check the response status code from the external API
            if response.status_code == 200:
                # Assume the API returns a JSON response
                api_response_data = response.json()
                
                # Handle the successful login response from the external API
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful',
                    'token': api_response_data.get('token')  # Assuming the external API returns a token
                }, status=200)
            else:
                # Handle invalid credentials or other errors from the external API
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid username or password'
                }, status=response.status_code)

        except requests.exceptions.RequestException as e:
            # Handle network or connection errors
            return JsonResponse({
                'status': 'error',
                'message': f'Error connecting to external API: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests are allowed'
    }, status=405)