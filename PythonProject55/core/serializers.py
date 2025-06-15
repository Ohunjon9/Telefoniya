from rest_framework import serializers
from .models import Abonent, Tarif, Tolov

class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = '__all__'

class AbonentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonent
        fields = '__all__'

class TolovSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tolov
        fields = '__all__'
