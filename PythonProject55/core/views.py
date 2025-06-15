from rest_framework import viewsets
from .models import Abonent, Tarif, Tolov
from .serializers import AbonentSerializer, TarifSerializer, TolovSerializer
from django.http import JsonResponse
from .models import Tarif  # Tarif modeli o'zgartirilgan nomga qarab

def tariflar_view(request):
    tariflar = Tarif.objects.all()  # Tariflarni olish
    tariflar_data = [{"id": tarif.id, "nomi": tarif.nomi, "narxi": tarif.narxi} for tarif in tariflar]
    return JsonResponse(tariflar_data, safe=False)

class TarifViewSet(viewsets.ModelViewSet):
    queryset = Tarif.objects.all()
    serializer_class = TarifSerializer

class AbonentViewSet(viewsets.ModelViewSet):
    queryset = Abonent.objects.all()
    serializer_class = AbonentSerializer

class TolovViewSet(viewsets.ModelViewSet):
    queryset = Tolov.objects.all()
    serializer_class = TolovSerializer
