# myapp/views.py

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

class LoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="User login",
        request_body=LoginSerializer,
        responses={200: "Login successful", 400: "Invalid credentials"},
        manual_parameters=[
            openapi.Parameter(
                'username', 
                openapi.IN_QUERY,  # Change to openapi.IN_FORM if you're using form data
                type=openapi.TYPE_STRING,
                description="Your username"
            ),
            openapi.Parameter(
                'password',
                openapi.IN_QUERY,  # Change to openapi.IN_FORM if you're using form data
                type=openapi.TYPE_STRING,
                description="Your password"
            ),
        ],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
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

                    print(api_response_data)
                    
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

            if user is not None:
                # login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }, status=405)
