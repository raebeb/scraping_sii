from rest_framework import serializers

class ClientSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    rut = serializers.CharField()
    address = serializers.CharField()
    date_of_construction = serializers.CharField()
    activity_start_date = serializers.CharField()
    current_legal_representatives = serializers.CharField()
    current_partners = serializers.CharField()
    current_economic_activities = serializers.CharField()
    characteristics = serializers.CharField()
    authorized_tax_documents = serializers.CharField()
