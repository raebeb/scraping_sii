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
        #TODO: 1 -> Create the client, 2 -> with the client created get the data from sii_scraper
        serializer = ClientSerializer(client)
        return Response(serializer.data)
