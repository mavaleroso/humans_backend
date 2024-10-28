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
        validated_response = NewlyHiredListRequest.execute(request)
        if validated_response['status_code'] == 200 :
            results = NewlyHiredListService.execute(validated_response)

            return JsonResponse({
                'status_code': 200,
                'status': 'success',
                'data': results['data']
            }, status=200) 
        else:
            return JsonResponse(validated_response, status=validated_response['status_code']) 

