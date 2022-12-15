# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from etude.models import Questionnaire, Questionpajsm, Reponsepajsm, Vignette, Intervenant, Centresante, Resultatenquete
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from etude.etude_constants import CHOIX_ON, CHOIX_ONUK, CHOIX_ONNSP, CHOIX_VFNSP, CHOIX_MOINSPLUS, CHOIX_UNDIX, \
    CHOIX_UNCINQ, CHOIX_UNSIX, CHOIX_UNCINQ2
from django.db.models import Q, Count
from django.template import loader
import csv
import datetime

DATE = datetime.datetime.now().strftime('%Y %b %d')


# Pour l'exportation en streaming du CSV
class Echo(object):
    # An object that implements just the write method of the file-like interface.
    def write(self, value):
        # Write the value by returning it, instead of storing in a buffer
        return value


## Prepare les syntaxes pour exportation / importation des donnees pour les stats
# Pour les syntaxes SPSS, fait le fichier des variables et des listes de valeurs
# Pour les syntaxes R, fait le fichier des listes de valeurs
def fait_entete_pajinter_R(request, questionnaire):
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteR_{}.txt"'.format(questionnaire)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions = extraction_requete_pajinter(questionnaire)
    typepresents = Questionpajsm.objects.values('typequestion__nom').order_by().filter(questionnaire_id=questionnaire). \
                                            exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                            annotate(tqcount=Count('typequestion__nom'))
    autresq = []
    if questionnaire == 101:
        # Socio-demo ajoute les donnees de la table Intervenants
        fields = Intervenant._meta.fields
        for field in fields:
            if field.name != "code" and field.name != "courriel":
                autresq.append(field.name)

    t = loader.get_template('R_pajinter_syntaxe.txt')
    response.write(t.render({'questions': questions, 'typequestions': typepresents, 'questionnaire': questionnaire, 'autresq': autresq}))
    return response

# Prepare la liste des questions du questionnaire selectionne
def extraction_requete_pajinter(questionnaire):
    # questionnaire_id > 100 et < 10 000
    questions = Questionpajsm.objects.filter(questionnaire_id=questionnaire). \
                                    exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                    order_by('questionno')
    return questions

## Première étape pour exporter les données par questionnaire.
# Scinde les données en paquets de (seuil) 150 dossiers si nécessaire
# appele par csv/<int:questionnaire>
# et prépare les urls pour procéder à l'extraction
# urls pour appeler ffait_csv, name='do_csv'
@login_required(login_url=settings.LOGIN_URI)
def prepare_csv(request, questionnaire, tous):
    nombre_personnes = Intervenant.objects.all().count()
    questionnaire_nom = Questionnaire.objects.get(pk=questionnaire)
    seuil = 150
    if nombre_personnes > seuil:
        reste = 0
        if nombre_personnes % seuil > 0:
            reste = 1
        iterations = int(nombre_personnes/seuil) + reste
    else:
        iterations = 1
    return render(request, 'page_extraction.html',
                      {
                       'iterations': range(iterations),
                       'questionnaire': questionnaire,
                       'questionnaire_nom': questionnaire_nom.nom_en,
                       'seuil': seuil,
                       'tous': tous
                      })


# Procede a l'exportation des donnees en CSV tab separated par questionnaire.
# appelé par page_extraction.html via url 'PAJSM/csv/<int:questionnaire>/<int:iteration>/'
# Necessite d'utiliser le streaming pour exporter les données
# Fait une ligne sans donnees si l'assistant a fait au moins un des questionnaires
def ffait_csv(request, questionnaire, iteration, seuil, tous):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    questions = Questionpajsm.objects.\
                        filter(questionnaire_id=questionnaire).\
                        exclude(Q(typequestion=7) | Q(typequestion=100)).\
                        order_by('questionno').values('id', 'varname')
    inf = iteration * seuil
    sup = (iteration + 1) * seuil
    if tous == 0:
        intervenants = Intervenant.objects.filter(completed=1).values('id', 'completed', 'vignette1', 'vignette2')[inf:sup]
    else:
        intervenants = Intervenant.objects.all().values('id', 'completed', 'vignette1', 'vignette2')[inf:sup]
    toutesleslignes = []

    if questionnaire == 101:
        # Socio-demo ajoute les donnees de la table Intervenants
        entete = []
        fields = Intervenant._meta.fields
        for field in fields:
            if field.name != "code" and field.name != "courriel":
                entete.append(field.name)
    elif questionnaire == 104:
        # Vignettes
        entete = ['ID', 'completed', 'vignette1', 'vignette2']
    else:
        entete = ['ID', 'completed']
    for question in questions:
        entete.append(question['varname'])
    entete.append('Date_Created_at')
    entete.append('Time_Created_at')
    entete.append('Date_Updated_at')
    entete.append('Time_Updated_at')
    toutesleslignes.append(entete)
    decompte = 0
    if questionnaire == 101:
        if tous == 1:
            intervenants = Intervenant.objects.all()[inf:sup]
        else:
            intervenants = Intervenant.objects.filter(completed=1)[inf:sup]
        fields = Intervenant._meta.fields
        for intervenant in intervenants:
            ligne = []
            for field in fields:
                if field.name != "code" and field.name != "courriel":
                    value = field.value_from_object(intervenant)
                    if value is None:
                        value = ""
                    ligne.append(value)
            for question in questions:
                try:
                    donnee = Resultatenquete.objects.filter(intervenant_id=intervenant.id,
                                                            question_id=question['id']).values('reponsetexte')
                except Resultatenquete.DoesNotExist:
                    donnee = None
                if donnee:
                    ligne.append(donnee[0]['reponsetexte'])
                else:
                    ligne.append('')
            decompte += 1
            toutesleslignes.append(ligne)
    else:
        for intervenant in intervenants:
            creatimestamps = []
            updatimestamps = []
            ligne = [intervenant['id'], intervenant['completed']]
            if Resultatenquete.objects.filter(intervenant_id=intervenant['id'], questionnaire_id=questionnaire).exists():
                if questionnaire == 104:
                    ligne.append(intervenant['vignette1'])
                    ligne.append(intervenant['vignette2'])
                for question in questions:
                    try:
                        donnee = Resultatenquete.objects.filter(intervenant_id=intervenant['id'], question_id=question['id']).values('reponsetexte', 'created_at', 'updated_at')
                    except Resultatenquete.DoesNotExist:
                        donnee = None
                    if donnee:
                        creatimestamps.append(donnee[0]['created_at'])
                        updatimestamps.append(donnee[0]['updated_at'])
                        ligne.append(donnee[0]['reponsetexte'])
                    else:
                        ligne.append('')
                creatimestamps.sort()
                updatimestamps.sort()
                ligne.append(creatimestamps[0].strftime('%Y-%m-%d'))
                ligne.append(creatimestamps[0].strftime('%H:%M:%S'))
                ligne.append(updatimestamps[-1].strftime('%Y-%m-%d'))
                ligne.append(updatimestamps[-1].strftime('%H:%M:%S'))
            decompte += 1

            toutesleslignes.append(ligne)
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = 'Datas_{}_{}_L{}.csv'.format(questionnaire, now, iteration)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                      content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response

