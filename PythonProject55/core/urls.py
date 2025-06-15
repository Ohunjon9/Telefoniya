from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AbonentViewSet, TarifViewSet, TolovViewSet
from django.urls import path
from . import views



router = DefaultRouter()
router.register(r'abonentlar', AbonentViewSet)
router.register(r'tariflar', TarifViewSet)
router.register(r'tolovlar', TolovViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tariflar/', views.tariflar_view, name='tariflar'),
]