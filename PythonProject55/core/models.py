from django.db import models

class Tarif(models.Model):
    nomi = models.CharField(max_length=100)
    narxi = models.DecimalField(max_digits=10, decimal_places=2)
    sana = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nomi

# models.py

class Abonent(models.Model):
    fio = models.CharField(max_length=100)
    telefon_raqami = models.CharField(max_length=15)
    tarif = models.ForeignKey(Tarif, on_delete=models.CASCADE)
    sana = models.DateField(auto_now_add=True)  # 'sana' field

    def __str__(self):
        return self.fio


class Tolov(models.Model):
    abonent = models.ForeignKey(Abonent, on_delete=models.CASCADE)
    sana = models.DateField(auto_now_add=True)
    summa = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.abonent.fio} - {self.summa} so'm"
