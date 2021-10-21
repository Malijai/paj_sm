# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Delits, Ages, Diagnostics, Decisions, Prerequis, Typetraitements, Echecs, Succes, Surveillances, Fins, Pajold
from .models import Exclus, References, Judiciaires, Conditions, Partenaires, Professionnels, Equipe, Reunions
from .models import Limites, Echecmotifs,Evaluations

#class DocumentInline(admin.StackedInline):
class EquipeInline(admin.TabularInline):
    model = Equipe
#    verbose_name_plural = "Les professionnels"
    fields = ['profession','nombre','duree','tache']



class TribunalAdmin(admin.ModelAdmin):
    fieldsets = [
        ('A- Description générale ', {'fields': [('nom', 'province'), 'adresse','siteweb',
                                     ('nomresponsable', 'formationresponsable','responcontact'),
                                     ('rapportannuel','tsmfile'),
                                     'debut','objectifs','clientele'
                                     ]}),
        ('B- Sélection des participants', {'fields': [('etapejudiciaire','etapejudiciairtxt'), ('reference','referencetxt'),
                                     ('prerequis','age'),
                                     ('diagnostic','typedelits','prerequistexte'),
                                     ('exclusions','exclusiontexte'),
                                     ('decision', 'decisionpouvoir'), 'delais']}),
        ('C- Fonctionnement', {'fields': [('traitementtype', 'traitementtexte','medication'),
                                          ('condition','conditiontexte'),
                                          ('respectcondition','reussitedef'),
                                          ('echec','echectexte'),
                                          ('succes','succestexte'),
                                          ('finbool','fintexte'),
                                          ('progdureebool','traitementduree','traitementmin','traitementmax')]}),
        ('D- Partenariats', {'fields': [('autreprogramme','autreprogramtexte','autreaffilie'),
                                        ('partenariat','partenariattexte')]}),
        ('S- Statistiques du programme', {'fields': [('limiteparticipants','partactif'),('autrejur','autrejurtext'),
                                        'partmoyen',('nbreussi','nbreussitxt'),
                                        ('nbechoue','nbechouetxt'),'echecmotif']}),

        ('Détails techniques et Évaluation', {'fields': [('territoire', 'affiliation'), 'communication',
                                        ('evaluation', 'evalquand', 'evaltype', 'evalqui', 'resume'),
                                        ('evaluationfuture', 'evafuturedetail')]}),
        ('P- Les professionnels', {'fields': ['reunionfreq', 'reunionpresence']}),
    ]

    inlines = [EquipeInline,]

    list_display = ('nom', 'province')

    list_filter = ['province','evaluation']


def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Pajold, TribunalAdmin)
admin.site.register(Delits)
admin.site.register(Ages)
admin.site.register(Diagnostics)
admin.site.register(Decisions)
admin.site.register(Prerequis)
admin.site.register(Typetraitements)
admin.site.register(Echecs)
admin.site.register(Succes)
admin.site.register(Surveillances)
admin.site.register(Fins)
admin.site.register(Exclus)
admin.site.register(References)
admin.site.register(Judiciaires)
admin.site.register(Conditions)
admin.site.register(Partenaires)
admin.site.register(Professionnels)
admin.site.register(Reunions)
admin.site.register(Limites)
admin.site.register(Echecmotifs)
admin.site.register(Evaluations)

