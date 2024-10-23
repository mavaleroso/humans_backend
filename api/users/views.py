from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

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
    def get(self, request):
        # DRF automatically gets the user from the token
        user = request.user
        
        # Return user details along with active session info
        return Response({
            'active': True,
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'image_path': user.image_path  # Assuming this field exists in your CustomUser model
        })
