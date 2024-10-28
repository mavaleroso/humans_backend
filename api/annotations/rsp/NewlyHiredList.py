
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

newlyhiredlist_schema = swagger_auto_schema(
    operation_description="Get Newly hired Staff list",
    tags=["RSP"],
    responses={
        200: openapi.Response(description="Success"),
        401: openapi.Response(description="Unauthorized, invalid token")
    }
)
