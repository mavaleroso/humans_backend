
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

logout_schema = swagger_auto_schema(
    operation_description="Log out the user by deleting their authentication token",
    tags=["Authentication"],
    responses={
        204: openapi.Response(description="Logout successful"),
        401: openapi.Response(description="Unauthorized, invalid token")
    }
)