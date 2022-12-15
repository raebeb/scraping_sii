from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import ClientSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class ClientViewSet(viewsets.ViewSet):
    def list(self, request):
        serializer = ClientSerializer()
        return Response(serializer.data)

    def retrieve(self, request):
        client = '' #TODO get client from scraped data
        serializer = ClientSerializer(client)
        return Response(serializer.data)
