from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import CompanySerializer
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.sii_user import SiiUser
from core.utils import get_company_data


class SIIDataViewSet(viewsets.ViewSet):
    def get_queryset(self):
        queryset = ""
        return queryset

    @swagger_auto_schema(
        method="get",
        operation_description="Get personal and tax data from SII",
        responses={
            200: CompanySerializer,
            400: "Invalid credentials"},
        manual_parameters=[
            openapi.Parameter(
                "rut",
                openapi.IN_QUERY,
                description="RUT",
                type=openapi.TYPE_STRING),
            openapi.Parameter(
                "password",
                openapi.IN_QUERY,
                description="Password",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=False, methods=["get"])
    def personal_and_tax_data(self, request):
        query_params = request.query_params
        rut = query_params.get("rut")
        password = query_params.get("password")
        sii_user = SiiUser(rut, password)

        if sii_user:
            company_data = get_company_data(sii_user)
            serializer = CompanySerializer(data=company_data)
            serializer.is_valid(raise_exception=True)
            return Response(company_data, 200)
        else:
            return Response("Invalid credentials", 400)
