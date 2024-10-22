from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
    return Response({'message': 'Hello, World!'})