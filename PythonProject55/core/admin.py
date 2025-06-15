from django.contrib import admin
from .models import Tarif, Abonent, Tolov

@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'narxi', 'sana')  # Add 'sana' to list display
    search_fields = ('nomi', 'narxi')
    list_filter = ('sana',)  # Add filter for 'sana'

@admin.register(Abonent)
class AbonentAdmin(admin.ModelAdmin):
    list_display = ('fio', 'telefon_raqami', 'tarif', 'sana')  # Add 'sana' to list display
    search_fields = ('fio', 'telefon_raqami', 'tarif')
    list_filter = ('fio', 'telefon_raqami', 'tarif', 'sana')  # Add filter for 'sana'

@admin.register(Tolov)
class TolovAdmin(admin.ModelAdmin):
    list_display = ('abonent', 'sana', 'summa')  # Add 'sana' to list display
    list_filter = ('abonent', 'sana', 'summa')  # Add filter for 'sana'
    search_fields = ('abonent__fio',)
