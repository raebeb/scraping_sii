from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import ClientSerializer
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

from core.sii_user import SiiUser
from core.utils import get_company_data

class SIIDataViewSet(viewsets.ViewSet):

    def get_queryset(self):
        queryset = ''
        return queryset

    def list(self, request):
        serializer = ClientSerializer()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def personal_and_tax_data(self, request):
        query_params = request.query_params
        rut = query_params.get('rut')
        password = query_params.get('password')
        sii_user = SiiUser(rut, password)

        if sii_user:
            company_data = get_company_data(sii_user)
            return Response(company_data)
        else:
            return Response("Invalid credentials")



