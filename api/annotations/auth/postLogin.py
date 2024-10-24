
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


login_schema = swagger_auto_schema(
    operation_description="User login endpoint",
    tags=["Authentication"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password of the user'),
        },
        required=['username', 'password']
    ),
    responses={
        200: openapi.Response(description="Login successful"),
        400: openapi.Response(description="Invalid credentials"),
        401: openapi.Response(description="Unauthorized")
    }
)
