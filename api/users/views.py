from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token

class CheckActiveSessionView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures the request is authenticated

    @swagger_auto_schema(
        operation_description="Check if the user has an active session. Use 'Token {your_token}' format.",
        tags=["Authentication"],
        security=[{'Token': []}],  # Reference the security scheme here
        responses={
            200: "Active session details",
            401: "Unauthorized, token invalid or expired"
        }
    )
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
