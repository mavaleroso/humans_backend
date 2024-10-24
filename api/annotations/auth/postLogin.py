
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        help_text="Your username",
        style={'input_type': 'text'},  # This makes it a text input
    )
    password = serializers.CharField(
        required=True,
        write_only=True,  # This prevents the password from being read back
        help_text="Your password",
        style={'input_type': 'password'},  # This makes it a password input (hidden)
    )

login_schema = swagger_auto_schema(
    operation_description="User login endpoint",
    request_body=LoginSerializer,
    responses={
        200: openapi.Response(description="Login successful", examples={"application/json": {"token": "jwt_token_here"}}),
        400: openapi.Response(description="Invalid credentials"),
        401: openapi.Response(description="Unauthorized")
    }
)
