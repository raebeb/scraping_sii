from rest_framework import serializers


class LegalRepresentativeSerializer(serializers.Serializer):
    name = serializers.CharField()
    rut = serializers.CharField()
    from_date = serializers.CharField()


class CurrentPartnerSerializer(serializers.Serializer):
    name = serializers.CharField()
    rut = serializers.CharField()
    aware_capital = serializers.IntegerField()
    capital_to_find_out = serializers.IntegerField()
    capital_percentage = serializers.FloatField()
    percentage_utilities = serializers.FloatField()
    membership_from = serializers.CharField()


class ActiveEconomicActivitySerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    category = serializers.IntegerField()
    taxable = serializers.BooleanField()
    start_at = serializers.CharField()


class CharacteristicSerializer(serializers.Serializer):
    start_at = serializers.CharField()
    description = serializers.CharField()


class CompanySerializer(serializers.Serializer):
    legal_representative = LegalRepresentativeSerializer(many=True)
    constitution_date = serializers.CharField()
    start_of_activities = serializers.CharField()
    full_address = serializers.CharField()
    current_partners = CurrentPartnerSerializer(many=True)
    active_economic_activities = ActiveEconomicActivitySerializer(many=True)
    characteristics = CharacteristicSerializer(many=True)
