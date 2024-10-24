
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

verifyToken_schema = swagger_auto_schema(
    operation_description="Check if the user has an active session. Use 'Token {your_token}' format.",
    tags=["Authentication"],
    security=[{'Token': []}],  # Reference the security scheme here
    responses={
        200: "Active session details",
        401: "Unauthorized, token invalid or expired"
    }
)