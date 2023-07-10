# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from etude.models import Questionnaire, Questionpajsm, Reponsepajsm, Resultatrepetpajsm, Resultatpajsm, Accompagnement, \
    Victime, Listevaleur, Typequestion, Personne, Pajsmlist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.db.models import Q, Count
from django.template import loader
import csv
import datetime
from django.core.files.storage import FileSystemStorage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

DATE = datetime.datetime.now().strftime('%Y %b %d')
NOM_FICHIER_PDF = "PAJ_SM.pdf"
TITRE = "PAJ_SM Data Entry Protocol"
PAGE_INFO = " Data protocol - Printed date: " + datetime.datetime.now().strftime('%Y/%m/%d')
PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()

# Pour l'exportation en streaming du CSV
class Echo(object):
    # An object that implements just the write method of the file-like interface.
    def write(self, value):
        # Write the value by returning it, instead of storing in a buffer
        return value

## Prepare les syntaxes pour exportation / importation des donnees pour les stats
# Pour les syntaxes SPSS, fait le fichier des variables et des listes de valeurs
# Pour les syntaxes R, fait le fichier des listes de valeurs
def fait_entete_pajsaisie_R(request, questionnaire):
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteR_{}.txt"'.format(questionnaire)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions = extraction_requete_pajsaisie(questionnaire)
    typepresents = Questionpajsm.objects.values('typequestion__nom').order_by().filter(questionnaire_id=questionnaire). \
                                            exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                            annotate(tqcount=Count('typequestion__nom'))
    autresq = []
    if questionnaire == 1:
        # Socio-demo ajoute les donnees de la table Personnes
        fields = Personne._meta.fields
        for field in fields:
            autresq.append(field.name)
    t = loader.get_template('R_pajinter_syntaxe.txt')
    response.write(t.render({'questions': questions, 'typequestions': typepresents, 'questionnaire': questionnaire, 'autresq': autresq}))
    return response

# Pour les syntaxes SPSS, fait le fichier des variables et des listes de valeurs
def fait_entete_spss(request, questionnaire):
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSPSS_{}.sps"'.format(questionnaire)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions = Questionpajsm.objects.filter(questionnaire_id=questionnaire).exclude(Q(typequestion=7) | Q(typequestion=100))
    autresq = []
    if questionnaire == 1:
        # Socio-demo ajoute les donnees de la table Personnes
        fields = Personne._meta.fields
        for field in fields:
            autresq.append(field.name)
    if questionnaire == 11:
        repet = 1
    else:
        repet = 0

    t = loader.get_template('spss_paj_syntaxe.txt')
    response.write(t.render({'questions': questions, 'repet': repet, 'autresq': autresq}))
    return response


# Prepare la liste des questions du questionnaire selectionne
def extraction_requete_pajsaisie(questionnaire):
    # questionnaire_id < 100
    questions = Questionpajsm.objects.filter(questionnaire_id=questionnaire). \
                                    exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                    order_by('questionno')
    return questions

## Première étape pour exporter les données par paj et par questionnaire.
# Scinde les données en paquets de (seuil) 150 dossiers si nécessaire
# appele par csvpaj/<int:paj>/<int:questionnaire>
# et prépare les urls pour procéder à l'extraction
# urls pour appeler ffait_csv, name='do_csv'
@login_required(login_url=settings.LOGIN_URI)
def prepare_csv_pajsaisie(request, paj, questionnaire, tous, seuil):
    nombre_personnes = Personne.objects.filter(selectedpaj_id=paj).count()
    questionnaire_nom = Questionnaire.objects.get(pk=questionnaire)
    # seuil = 40
    pajsm = Pajsmlist.objects.get(pk=paj)
    if nombre_personnes > seuil:
        reste = 0
        if nombre_personnes % seuil > 0:
            reste = 1
        iterations = int(nombre_personnes/seuil) + reste
    else:
        iterations = 1
    return render(request, 'page_extractionsaisie.html',
                      {
                       'iterations': range(iterations),
                       'questionnaire': questionnaire,
                       'questionnaire_nom': questionnaire_nom.nom_en,
                       'seuil': seuil,
                       'tous': tous,
                       'paj': pajsm,
                      })

# Procede a l'exportation des donnees en CSV tab separated par paj et questionnaire.
# appelé par page_extractionsaisie.h tml via url 'csvpaj/<int:paj>/<int:questionnaire>/<int:iteration>/<int:seuil>/<int:tous>/'
#'ffait_csv_pajsaisie'  paj.id questionnaire iteration seuil tous
# Necessite d'utiliser le streaming pour exporter les données
# Fait une ligne sans donnees si l'assistant a fait au moins un des questionnaires
def ffait_csv_pajsaisie(request, paj, questionnaire, iteration, seuil, tous):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    questions = Questionpajsm.objects.\
                        filter(questionnaire_id=questionnaire).\
                        exclude(Q(typequestion=7) | Q(typequestion=100)).\
                        order_by('questionno').values('id', 'varname')
    accompagnements = Accompagnement.objects.all()
    inf = iteration * seuil
    sup = (iteration + 1) * seuil
    if tous == 0:
        personnes = Personne.objects.filter(completed=1, selectedpaj=paj).values('id', 'completed')[inf:sup]
    else:
        personnes = Personne.objects.filter(selectedpaj=paj).values('id', 'completed')[inf:sup]
    toutesleslignes = []

    if questionnaire == 1:
        # Socio-demo ajoute les donnees de la table Personnes
        entete = []
        fields = Personne._meta.fields
        for field in fields:
            if field.name != "code" and field.name != "courriel":
                entete.append(field.name)
    elif questionnaire < 10:
        entete = ['ID', 'completed', 'accompagnement']
    else:
        entete = ['ID', 'completed', 'accompagnement','fiche']

    for question in questions:
        entete.append(question['varname'])
    toutesleslignes.append(entete)
    decompte = 0
    if questionnaire == 1:
        fields = Personne._meta.fields
        for personne in personnes:
            ligne = []
            for field in fields:
                if field.name != "code" and field.name != "courriel":
                    value = field.value_from_object(personne)
                    if value is None:
                        value = ""
                    ligne.append(value)
            for question in questions:
                try:
                    donnee = Resultatpajsm.objects.filter(personne_id=personne.id,
                                                            question_id=question['id']).values('reponsetexte')
                except Resultatpajsm.DoesNotExist:
                    donnee = None
                if donnee:
                    ligne.append(donnee[0]['reponsetexte'])
                else:
                    ligne.append('')
            decompte += 1
            toutesleslignes.append(ligne)
    elif questionnaire < 10:
        for personne in personnes:
            for accompagnement in accompagnements:
             if Resultatpajsm.objects.filter(personne_id=personne['id'], accompagnement_id=accompagnement).exists():
                    ligne = [personne['id'], personne['completed'], accompagnement.id]
                    for question in questions:
                        try:
                            donnee = Resultatpajsm.objects.filter(personne_id=personne['id'], question_id=question['id'], accompagnement_id=accompagnement).values('reponsetexte')
                        except Resultatpajsm.DoesNotExist:
                            donnee = None
                        if donnee:
                            ligne.append(donnee[0]['reponsetexte'])
                        else:
                            ligne.append('')

                    toutesleslignes.append(ligne)
            decompte += 1
    else:
        for personne in personnes:
            for accompagnement in accompagnements:
                donnees = Resultatrepetpajsm.objects.order_by(). \
                                        filter(personne_id=personne['id'], accompagnement_id=accompagnement). \
                                        values_list('fiche', flat=True).distinct()
                if donnees.count() > 0:
                    for card in donnees:
                        ligne = [personne['id'], personne['completed'], accompagnement.id, card]
                        for question in questions:
                            try:
                                resultat = Resultatrepetpajsm.objects. \
                                    filter(personne_id=personne['id'], question_id=question['id'], fiche=card,
                                           accompagnement_id=accompagnement). \
                                    values('reponsetexte')
                            except Resultatrepetpajsm.DoesNotExist:
                                resultat = None
                            if resultat:
                                ligne.append(resultat[0]['reponsetexte'])
                                decompte += 1
                            else:
                                ligne.append('')
                        toutesleslignes.append(ligne)

    now = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = 'Datas_{}_{}_L{}.csv'.format(questionnaire, now, iteration)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                      content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response


def fait_csv_repetitive(personne, questions, card, accompagnement, completed):
    ligne = [personne, completed, accompagnement, card]
    decompte = 0
    for question in questions:
        try:
            donnee = Resultatrepetpajsm.objects. \
                filter(personne_id=personne, question_id=question['id'], fiche=card, accompagnement_id=accompagnement). \
                values('reponsetexte')
        except Resultatrepetpajsm.DoesNotExist:
            donnee = None
    if donnee:
        ligne.append(donnee[0]['reponsetexte'])
        decompte += 1
    else:
        ligne.append('rien')
    return ligne, decompte


#Exportation des questions en PDF
def myFirstPage(patron, _):
    patron.saveState()
    patron.setFont('Helvetica',16)
    patron.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, TITRE)
    patron.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 130, DATE)
    patron.setFont('Helvetica',10)
    patron.setStrokeColorRGB(0, 0, 0)
    patron.setLineWidth(0.5)
    patron.line(0, 65, PAGE_WIDTH - 0, 65)
    patron.drawString(inch, 0.70 * inch, "PAJ-SM / %s" % PAGE_INFO)
    patron.restoreState()


def myLaterPages(patron, doc):
    patron.saveState()
    patron.setFont('Helvetica',10)
    patron.setStrokeColorRGB(0, 0, 0)
    patron.setLineWidth(0.5)
    patron.line(0, 65, PAGE_WIDTH - 0, 65)
    patron.drawString(inch, 0.70 * inch, "Page %d %s" % (doc.page, PAGE_INFO))
    patron.restoreState()


@login_required(login_url=settings.LOGIN_URI)
def questions_pdf(request, questionnaire):
    fichier = 'QID_' + str(questionnaire) + '_' + NOM_FICHIER_PDF
#    doc = SimpleDocTemplate("/tmp/{}".format(NOM_FICHIER_PDF))
    doc = SimpleDocTemplate("/tmp/{}".format(fichier))
    questionnaire=Questionnaire.objects.get(pk=questionnaire)
    Story = [Spacer(1,1.5 * inch)]
    Story.append(Paragraph(questionnaire.nom_en, styles["Heading1"]))
    Story.append(Spacer(1, 0.5 * inch))
#    Story = [] # (si on ne veut pas de premiere page differente on ne met pas d'Espace en haut de la 1ere)
    style = styles['Code']
    bullettes = styles['Code']
#    articles_list = Article.objects.all()
#    for article in articles_list:
#    im = '<img src="media/images/pointblanc.jpg"/>'
    viol = 0
    for question in Questionpajsm.objects.filter(questionnaire_id=questionnaire):
        if question.typequestion.nom == 'TITLE':
            ptext = "<b>{}</b>".format(question.questionen)
            Story.append(Spacer(1, 0.2 * inch))
            Story.append(Paragraph(ptext, styles["Heading3"]))
            Story.append(Paragraph(".&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Question text", styles["Normal"]))
        elif question.typequestion.nom == 'COMMENT':
            ptext = "<b>{}</b>".format(question.questionen)
            Story.append(Paragraph(ptext, styles["Heading4"]))
            Story.append(Paragraph(".&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Question text", styles["Normal"]))
        else:
            x = 15 - len(question.varname)
            espace = ''
            for i in range(0, x):
                espace = espace + '&nbsp;'
            bogustext = question.varname + espace + question.questionen
            p = Paragraph(bogustext, style)
            Story.append(p)
        if question.typequestion.nom == "DICHO" or question.typequestion.nom == "DICHON" or question.typequestion.nom == "DICHOU":
            liste = [(1, 'Yes'), (0, 'No'), (98, 'NA'), (99, 'Unknown')]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "BOOLEAN":
            liste = [(1, 'Yes mentioned'), (3, 'maybe but not explicit'), (100, 'No not mentioned'), (98, 'NA'), (99, 'Unknown')]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "CATEGORIAL":
            liste = Reponsepajsm.objects.filter(question_id=question.id )
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list.reponse_valeur) + '&nbsp;&nbsp;' + str(list.reponse_en)
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "VICTIME":
            liste = Victime.objects.all()
            for list in liste:
                espace = '&nbsp;' * 25 + '&#x00B7;'
                bogustext = '&#124;' + espace + str(list.reponse_valeur) + '&nbsp;&nbsp;' + str(list.reponse_en)
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "PAYS" or question.typequestion.nom == "LANGUE":
            bogustext = '&#124;' + '&nbsp;' * 20 + "Stat can list of Countries or Languages"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    fs = FileSystemStorage("/tmp")
    with fs.open(fichier) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(fichier)
    return response

