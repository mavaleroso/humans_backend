from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from api.annotations.users.postVerifyToken import verifyToken_schema

class CheckActiveSessionView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures the request is authenticated


    @verifyToken_schema
    def post(self, request):
        # DRF automatically gets the user from the token
        user = request.user

        token, created = Token.objects.get_or_create(user=user)
        
        # Return user details along with active session info
        return Response({
            'api_token': token.key,
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'image_path': user.image_path,
            'position': user.position,
            'division': user.division,
            'section': user.section,
        })
