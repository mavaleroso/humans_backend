from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
import os
from django.contrib.auth import get_user_model
from api.models import CustomUser
from django.utils import timezone
from rest_framework.authtoken.models import Token

User = get_user_model() 

class LoginAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication"],
        operation_description="User login",
        request_body=LoginSerializer,
        responses={200: "Login successful", 400: "Invalid credentials"},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # External API endpoint URL
            portal_api_login = os.getenv('PORTAL_API_LOGIN')
            
            # Send a POST request to the external API
            try:
                response = requests.post(portal_api_login, data={
                    'username': username,
                    'password': password
                })

                
                # Check the response status code from the external API
                if response.status_code == 200:
                    # Assume the API returns a JSON response
                    api_response_data = response.json()

                    api_key = api_response_data['key']
                    request.session['key'] = api_key

                    portal_api_employee_details = os.getenv('PORTAL_API_EMPLOYEE_DETAILS')

                    try:
                        user = User.objects.get(username=username)
                        user.last_login = timezone.now()
                        user.save()
                    except User.DoesNotExist:
                        response_employee_details = requests.get(f"{portal_api_employee_details}{username}", headers={
                            'Authorization': f"Token {api_key}"
                        })

                        if response_employee_details.status_code == 200:
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

                        else: 
                            return JsonResponse({
                                'status': 'error',
                                'message': 'No user found in portal'
                            }, status=response_employee_details.status_code)
                    
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
                    }

                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login successful',
                        'token': token.key,
                        'data': user_data
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


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Log out the user by deleting their authentication token",
        tags=["Authentication"],
        responses={204: "Logout successful", 401: "Unauthorized, invalid token"}
    )
    def post(self, request):
        try:
            # Get the token associated with the authenticated user
            token = Token.objects.get(user=request.user)
            # Delete the token (logout)
            token.delete()

            return Response({"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)