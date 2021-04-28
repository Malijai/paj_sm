from django.contrib import admin
from .models import Centresante, Intervenant

class CentresanteAdmin(admin.ModelAdmin):
    model = Centresante
    can_delete = False


class IntervenantAdmin(admin.ModelAdmin):
    model = Intervenant
    readonly_fields = ('courriel', 'code')
    fields = ['courriel','concented','code']
    list_display = ('courriel', 'concented', 'centresante')
    list_filter = ['centresante', 'concented']
    can_delete = False


admin.site.register(Centresante, CentresanteAdmin)
admin.site.register(Intervenant, IntervenantAdmin)
