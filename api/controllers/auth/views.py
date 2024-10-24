
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from api.annotations.auth.postLogin import login_schema
from api.annotations.auth.postLogout import logout_schema
from api.services.auth.loginService import LoginService
from api.requests.auth.LoginRequest import LoginRequest
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @login_schema
    def post(self, request):
        validated_response = LoginRequest.execute(request)
        if validated_response['status_code'] == 200 :
            results = LoginService.execute(validated_response)
            return JsonResponse({
                'status_code': 200,
                'status': 'success',
                'data': results
            }, status=200) 
        else:
            return JsonResponse(validated_response, status=validated_response['status_code']) 

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @logout_schema
    def post(self, request):
        try:
            # Get the token associated with the authenticated user
            token = Token.objects.get(user=request.user)
            # Delete the token (logout)
            token.delete()

            return Response({"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)