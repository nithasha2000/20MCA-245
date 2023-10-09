from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getData(request):
    person={'name':'nithasha','age':23}
    return Response(person)