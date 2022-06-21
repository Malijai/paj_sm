from django.contrib import admin
from .models import Centresante, Intervenant, Personne

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


class PersonneAdmin(admin.ModelAdmin):
    list_display = ('code', 'selectedpaj', 'completed', 'date_indexh')
    list_filter = ['selectedpaj', 'completed',]
    actions = ['ouvre_dossier']

    def ouvre_dossier(self, request, queryset):
        rows_updated = queryset.update(completed=0)
        if rows_updated == 1:
            message_bit = "1 dossier a été"
        else:
            message_bit = "%s dossiers ont été" % rows_updated
        self.message_user(request, "%s réouvert(s)." % message_bit)
    ouvre_dossier.short_description = "Réouvrir les dossiers cochés"

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Centresante, CentresanteAdmin)
admin.site.register(Intervenant, IntervenantAdmin)
admin.site.register(Personne, PersonneAdmin)