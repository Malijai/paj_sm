from django.contrib import admin
from .models import Delits, Ages, Diagnostics, Decisions, Prerequis, Typetraitements, Echecs, Succes, Surveillances, Fins, Pajnew
from .models import Exclus, References, Judiciaires, Conditions, Partenaires, Professionnels, Equipe, Reunions
from .models import Limites, Echecmotifs,Evaluations,Echecconditions, Public, Document, Historique

#class DocumentInline(admin.StackedInline):
class EquipeInline(admin.TabularInline):
    model = Equipe
#    verbose_name_plural = "Les professionnels"
    fields = ['profession','nombre','duree','tache']

#class DocumentInline(admin.StackedInline):
class DocumentsInline(admin.TabularInline):
    model = Document
    verbose_name = "Documentation utile (autres documents)"
    verbose_name_plural = "Documentation utile (autres documents)"
#    verbose_name_plural = "Les professionnels"
    fields = ['titrecourt','documentation']


class HistoriqueInline(admin.TabularInline):
        model = Historique
        verbose_name = "Description des modifications importantes"
        verbose_name_plural = "Description des modifications importantes"
        #    verbose_name_plural = "Les professionnels"
        fields = ['modifhistoire',]



class PajAdmin(admin.ModelAdmin):
    fieldsets = [
        ('A- Identification du programme ou protocole ',
         {'fields': [('nom', 'sigle'), 'adresse', 'siteweb',
                     ('nomresponsable', 'titreresponsable', 'formationresponsable'),
                     ('courrielresponsable', 'telresponsable'),
                     'nomrepondant', ('courrielrepondant', 'telrepondant'),
                     ('territoire', 'municipalites','affiliation'),
                     ('confidentiel', 'public'),
                     ('rapportannuel', 'tsmfile', 'rapportannuelpublic'),
                     ('cadreref','cadrerefpublic'),
                     'debut', 'objectifs', 'clientele'
                     ]}),
        ('B- Référencement, sélection et admissibilité des participants',
         {'classes': ['collapse'], 'fields': [('etapejudiciaire', 'etapejudiciairtxt'), ('reference', 'referencetxt'),
                     ('prerequis', 'prerequistexte'),
                     ('age', 'typedelits'),
                     ('exclusions', 'exclusiontexte'),
                     'decision', 'decisionpouvoir']}),
        ('C- Fonctionnement',
         {'classes': ['collapse'], 'fields': [('delais', 'traitementtype', 'traitementtexte'),
                     ('condition', 'conditiontexte'),
                     'respectcondition',
                     ('echeccondition', 'echecconditiontexte'),
                     ('echecmotif', 'echectexte'),
                     ('succes', 'succestexte'),
                     ('finbool', 'fintexte'),
                     ('progdureebool', 'traitementduree', 'traitementmin', 'traitementmax')]}),
        ('D- Partenariats',
         {'classes': ['collapse'], 'fields': [('autreprogramme', 'autreprogramtexte', 'autreaffilie'),
                     ('partenariat', 'partenariattexte')]}),
        ('S- Roulement',
         {'classes': ['collapse'], 'fields': [('limiteparticipants', 'limitenb'),
                     ('partactif', 'caseload'),
                     ('autrejur','autrejurtext'),
                     'partmoyen',('nbreussi', 'nbreussitxt', 'nbechoue'),
                     ('nbsuccesdebut','nbechouedebut')]}),
        ('Évaluations et études',
         {'classes': ['collapse'],'fields': [('evaluation', 'evalquand', 'evalqui', 'evaltype', 'resume'),
                     ('evaluationfuture', 'evafuturedetail')]}),
        ('P- Équipe',
                {'classes': ['collapse'], 'fields': ['reunionfreq', 'audiencefreq', 'equipenb']}),
    ]

    inlines = [EquipeInline, DocumentsInline, HistoriqueInline]


def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Pajnew, PajAdmin)
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
admin.site.register(Echecconditions)
admin.site.register(Public)
