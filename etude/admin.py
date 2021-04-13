from django.contrib import admin
from .models import Centresante

class CentresanteAdmin(admin.ModelAdmin):
    model = Centresante
    can_delete = False


admin.site.register(Centresante, CentresanteAdmin)
