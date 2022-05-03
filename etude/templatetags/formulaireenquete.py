from django import template
import re
from django.apps import apps
from etude.models import Typequestion, Listevaleur, Reponsepajsm
from django import forms
from etude.etude_constants import CHOIX_ONUK, CHOIX_ON, CHOIX_ONNSP, CHOIX_VFNSP, CHOIX_MOINSPLUS, CHOIX_UNDIX, CHOIX_UNCINQ, CHOIX_UNCINQ2, CHOIX_UNSIX, CHOIX_ETUDIANT

register = template.Library()


@register.simple_tag
def fait_radioboutons(a, b, *args, **kwargs):
    qid = a
    sorte = b
    relation = kwargs['relation']
    cible = kwargs['cible']

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    liste = ()
    if sorte == "DICHO":
        liste = CHOIX_ON.items()
    elif sorte == "ONNSP":
        liste = CHOIX_ONNSP.items()
    elif sorte == "MOINSPLUS":
        liste = CHOIX_MOINSPLUS.items()
    elif sorte == "UNDIX":
        liste = CHOIX_UNDIX.items()
    elif sorte == "UNCINQ":
        liste = CHOIX_UNCINQ.items()
    elif sorte == "UNSIX":
        liste = CHOIX_UNSIX.items()
    elif sorte == "UNCINQ2":
        liste = CHOIX_UNCINQ2.items()
    elif sorte == "ETUDIANT":
        liste = CHOIX_ETUDIANT.items()
    else:
        liste = CHOIX_ONUK.items()
    question = forms.RadioSelect(choices=liste, attrs={'id': idcondition,})
    default = ''
    texte = enlevelisttag(question.render(name, default))
    texte = ajoutespan(texte)
    texte = ('<div class="radio-toolbar">{}</div>'.format(texte))

    return texte


@register.simple_tag
def fait_court(a, b, *args, **kwargs):
    qid = a
    relation = kwargs['relation']
    cible = kwargs['cible']

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)

    court_liste = [(1, 'Municipal'), (2, 'Provincial'), (3, 'Superior'), (99, 'Unknown')]
    question = forms.Select(choices=court_liste, attrs={'id': idcondition, })
    default = ''
    #return enlevelisttag(question.render(name,default))
    return question.render(name, default)


@register.simple_tag
def fait_date(qid, b, *args, **kwargs):
    relation = kwargs['relation']
    cible = kwargs['cible']
    an = ''
    mois = ''
    jour = ''

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    day, month, year = fait_select_date(idcondition, 1960, 2024)
#   name=q69_year, id=row...

    return year.render(name + '_year', an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


@register.simple_tag
def fait_textechar(qid, sorte, *args, **kwargs):
    relation = kwargs['relation']
    cible = kwargs['cible']
    classe =  kwargs['classe']

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)

    if sorte == 'STRING' or sorte == 'TIME':
        question = forms.TextInput(attrs={'size': 30, 'id': idcondition, 'class': classe, 'placeholder': "Texte"})
    else:
        question = forms.NumberInput(attrs={'size': 30, 'id': idcondition, 'class': classe, 'placeholder': "Nombre"})
    default = ''
    return question.render(name, default)


@register.simple_tag
def fait_duree(qid, sorte, *args, **kwargs ):
    relation = kwargs['relation']
    cible = kwargs['cible']
    langue =  kwargs['langue']
    an = ''
    mois = ''
    jour = ''

    years = {x: x for x in range(0, 20)}
    years[''] = ''
    days = {x: x for x in range(0, 32)}
    days[''] = ''
    months = {x: x for x in range(0, 13)}
    months[''] = ''
    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)

    year = forms.Select(choices=years.items(), attrs={'id': idcondition, 'name': name + '_year'})
    month = forms.Select(choices=months.items(), attrs={'name': name + '_month'})
    day = forms.Select(choices=days.items(), attrs={'name': name + '_day'})
    #return day, month, year
    return year.render(name + '_year', an) + ' Années ' + month.render(name + '_month', mois) + ' Mois ' + day.render(name + '_day', jour) + ' Jours '



@register.simple_tag
def fait_table(qid, sorte, *args, **kwargs):
    # questid sorte
    relation = kwargs['relation']
    cible = kwargs['cible']

    idcondition = fait_id(qid, cible, relation=relation)

    sorteq = Typequestion.objects.get(nom=sorte)
    listevaleurs = Listevaleur.objects.filter(typequestion=sorteq)
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')
    texte = ""
    default = ''
    if listevaleurs.count() > 4:
        liste.append(('', ''))
        question = forms.Select(choices=liste, attrs={'id': idcondition,})
        texte = question.render(name, default)
    else:
        question = forms.RadioSelect(choices=liste, attrs={'id': idcondition, })
        texte = enlevelisttag(question.render(name, default))
        texte = ajoutespan(texte)
        texte = ('<div class="radio-toolbar">{}</div>'.format(texte))

    return texte


@register.simple_tag
def fait_reponse(qid, b, *args, **kwargs):
    #   Pour listes de valeurs specifiques a chaque question
    relation = kwargs['relation']
    cible = kwargs['cible']

    idcondition = fait_id(qid, cible, relation=relation)

    listevaleurs = Reponsepajsm.objects.filter(question_id=qid, )
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')
    default = ''
    if listevaleurs.count() > 4:
        liste.append(('', ''))
        question = forms.Select(choices=liste, attrs={'id': idcondition,})
        texte = question.render(name, default)
    else:
        question = forms.RadioSelect(choices=liste, attrs={'id': idcondition, })
        texte = enlevelisttag(question.render(name, default))
        texte = ajoutespan(texte)
        texte = ('<div class="radio-toolbar">{}</div>'.format(texte))
    return texte


    #   Utlitaires generaux
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def enlevelisttag(texte):
    #   pour mettre les radiobutton sur une seule ligne
    texte = re.sub(r"(<ul[^>]*>)", r"", texte)
    texte = re.sub(r"(<li[^>]*>)", r"", texte)
    texte = re.sub(r"(</li>)", r"", texte)
    return re.sub(r"(</ul>)", r" ", texte)


def ajoutespan(texte):
    return re.sub(r">\n(.+)</label>", r"><span>\1</span></label>", texte)


def enlevebullets(texte):
    #   pour mettre les radiobutton sur une seule ligne
    return re.sub(r'<ul', r'<ul style="list-style-type:none;"', texte)


def fait_id(qid, cible, *args, **kwargs):
    #   fail l'ID pour javascripts ou autre
    relation = kwargs['relation']
    idcondition = "q" + str(qid)
    if relation != '' and cible != '':
        idcondition = 'row-{}X{}X{}'.format(qid, relation, cible)
    return idcondition


def fait_liste_tables(listevaleurs, sorte):
    liste = []
    for valeur in listevaleurs:
        if sorte == 'reponse':
            val = valeur.reponse_valeur
            nen = valeur.reponse_en
            liste.append((val, nen))
        elif sorte == 'violation':
            val = str(valeur.reponse_valeur)
            nen = val + ' - ' + valeur.reponse_en
            liste.append((val, nen))
    return liste


def fait_select_date(idcondition, name, deb, fin):
    years = {x: x for x in range(deb, fin)}
    years[''] = ''
    years['99'] = 'UKN'
    days = {x: x for x in range(1, 32)}
    days[''] = ''
    days['99'] = 'UKN'

    months = (('', ''), (1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'),
              (9, 'Sept'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec'), ('99', 'UKN'))
    year = forms.Select(choices=years.items(), attrs={'id': idcondition, 'name': name + '_year'})
    month = forms.Select(choices=months, attrs={'name': name + '_month'})
    day = forms.Select(choices=days.items(), attrs={'name': name + '_day'})
    return day, month, year

