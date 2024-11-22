from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from api.annotations.users.postVerifyToken import verifyToken_schema
from api.requests.rsp.NewlyHiredListRequest import NewlyHiredListRequest
from api.services.rsp.NewlyHiredListService import NewlyHiredListService
from api.annotations.rsp.NewlyHiredList import newlyhiredlist_schema
from django.http import JsonResponse

class CheckActiveSessionView(APIView):
    # permission_classes = [IsAuthenticated]

    @newlyhiredlist_schema
    def get(self, request):
        page = request.GET.get('page', 1)
        validated_response = NewlyHiredListRequest.execute(request,page)
    
        results = NewlyHiredListService.execute(validated_response)

        return JsonResponse(results)
