import imp
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.


def index(request):
    return HttpResponse('<h1>Starting the chat App.</h1>')


class HelloApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello from Api.. It\'s Working.'}
        return Response(content)
