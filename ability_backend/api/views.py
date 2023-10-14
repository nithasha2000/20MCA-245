from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(request):
    return Response("Starting the app")


@api_view(['POST'])
def login(request):
    response_data = JSONParser().parse(request)
    return Response(f"New request {response_data}")