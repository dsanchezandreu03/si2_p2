# admin.py
from django.contrib import admin
from .models import Tarjeta, Pago 

# Register Tarjeta model
@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):
    pass

# Register Voto model
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    pass