from django import template
import re
from django.apps import apps
from etude.models import Reponsepajsm, Resultatpajsm, Personne, Typequestion, Listevaleur, Victime, Accompagnement, Pajsmlist
from django import forms
from etude.etude_constants import CHOIX_ONUK, CHOIX_ON
from accueil.models import User, Paj

register = template.Library()


@register.simple_tag
def fait_dichou(a, b, *args, **kwargs):
    qid = a
    sorte = b
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    defaultvalue = fait_default(personneid, qid, accompagnement=accompagnement)
    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    if sorte == "DICHO":
        liste = CHOIX_ON.items()
        question = forms.RadioSelect(choices=liste, attrs={'id': idcondition,' name': name, })
    else:
        liste = CHOIX_ONUK.items()
        question = forms.RadioSelect(choices=liste, attrs={'id': idcondition, 'name': name, })

    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_court(a, b, *args, **kwargs):
    qid = a
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    defaultvalue = fait_default(personneid, qid, accompagnement=accompagnement)
    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)

    court_liste = [(1, 'Municipal'), (2, 'Provincial'), (3, 'Superior'), (99, 'Unknown')]
    question = forms.Select(choices=court_liste, attrs={'id': idcondition, 'name': name, })

    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_date(qid, b, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    an = ''
    mois = ''
    jour = ''
    if Resultatpajsm.objects.filter(personne__id=personneid, question__id=qid, accompagnement_id=accompagnement).exists():
        ancienne = Resultatpajsm.objects.get(personne__id=personneid, question__id=qid, accompagnement_id=accompagnement).__str__()
        an, mois, jour = ancienne.split('-')

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    day, month, year = fait_select_date(idcondition, name, 1960, 2024)
#   name=q69_year, id=row...

    return year.render(name + '_year', an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


@register.simple_tag
def fait_datecode(qid, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    varname = kwargs['varname']
    an = ''
    mois = ''
    jour = ''
    ancienne = ''

    personne = Personne.objects.get(pk=personneid)
    if personne.__dict__[varname] is not None:
        ancienne = 1

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    day, month, year = fait_select_date(idcondition, name, 1920, 2005)
#    name=q69_year, id=row...
    if ancienne:
        return 'Already Encrypted data'
    else:
        return year.render(name + '_year', an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


@register.simple_tag
def fait_textechar(qid, sorte, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    defaultvalue = fait_default(personneid, qid, accompagnement=accompagnement)
    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)

    if sorte == 'STRING' or sorte == 'TIME':
        question = forms.TextInput(attrs={'size': 30, 'id': idcondition, 'name': name})
    else:
        question = forms.NumberInput(attrs={'size': 30, 'id': idcondition, 'name': name})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_codetexte(qid, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    varname = kwargs['varname']
    ancienne = ''
    personne = Personne.objects.get(pk=personneid)
    if personne.__dict__[varname] is not None:
        ancienne = 1

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    if ancienne:
        return 'Already Encrypted data'
    else:
        question = forms.TextInput(attrs={'size': 30, 'id': idcondition, 'name': name})
        return question.render(name, '')


@register.simple_tag
def fait_table(qid, sorte, *args, **kwargs):
    #   questid sorte
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    defaultvalue = fait_default(personneid, qid, accompagnement=accompagnement)
    idcondition = fait_id(qid, cible, relation=relation)

    sorteq = Typequestion.objects.get(nom=sorte)
    listevaleurs = Listevaleur.objects.filter(typequestion=sorteq)
    name = "q" + str(qid)
    if sorte == "VIOLATION":
        liste = fait_liste_tables(listevaleurs, 'violation')
    else:
        liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition, 'name': name})
    return question.render(name, defaultvalue)


@register.simple_tag
def fait_reponse(qid, b, *args, **kwargs):
    #   Pour listes de valeurs specifiques a chaque question
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    defaultvalue = fait_default(personneid, qid, accompagnement=accompagnement)
    idcondition = fait_id(qid, cible, relation=relation)

    listevaleurs = Reponsepajsm.objects.filter(question_id=qid, )
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition, 'name': name})
    #   return question.render(name, defaultvalue)
    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_victimes(qid, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    defaultvalue = fait_default(personneid, qid, accompagnement=accompagnement)
    idcondition = fait_id(qid, cible, relation=relation)

    listevaleurs = Victime.objects.all()
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition, 'name': name})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_table_valeurs_prov(qid, sorte, *args, **kwargs):
    #   pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur
    #   et dont la liste depend de la province
    province = kwargs['province']
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    sortetable = {"ETABLISSEMENT": "etablissement", "MUNICIPALITE": "municipalite"}
    tableext = sortetable[sorte]
    # assistant = kwargs['uid']
    accompagnement = kwargs['accompagnement']

    defaultvalue = fait_default(personneid, qid, accompagnement=accompagnement)
    idcondition = fait_id(qid, cible, relation=relation)

    klass = apps.get_model('dataentry', tableext)
    #   klass = apps.get_model('dataentry', sortetable[b])
    listevaleurs = klass.objects.filter(province__id=province)
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition, 'name': name})

    return question.render(name, defaultvalue)

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


def fait_default(personneid, qid,  *args, **kwargs):
    #   fail la valeur par deffaut
    # assistant = kwargs['assistant']
    accompagnement = kwargs['accompagnement']
    ancienne = ''
    if Resultatpajsm.objects.filter(personne__id=personneid, question__id=qid, accompagnement_id=accompagnement).exists():
        ancienne = Resultatpajsm.objects.get(personne__id=personneid, question__id=qid, accompagnement_id=accompagnement).__str__()
    return ancienne


def fait_id(qid, cible, *args, **kwargs):
    #   fail l'ID pour javascripts ou autre
    relation = kwargs['relation']
    idcondition = "q" + str(qid)
    if relation != '' and cible != '':
        idcondition = 'row-{}X{}X{}'.format(qid, relation, cible)
    return idcondition


def fait_liste_tables(listevaleurs, sorte):
    liste = [('', '')]
    for valeur in listevaleurs:
        if sorte == 'reponse':
            val = valeur.reponse_valeur
            nen = valeur.reponse_en
            liste.append((val, nen))
        elif sorte == 'violation':
            val = str(valeur.reponse_valeur)
            nen = val + ' - ' + valeur.reponse_en
            liste.append((val, nen))
        else:
            val = str(valeur.id)
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


    #   pour les questions de Personne
@register.simple_tag
def creetextechar(qid, sorte, *args, **kwargs):
    name = "q" + str(qid)

    if sorte == 'STRING' or sorte == 'CODESTRING':
        question = forms.TextInput(attrs={'size': 30, 'id': name, 'name': name})
    else:
        question = forms.NumberInput(attrs={'size': 30, 'id': name, 'name': name})

    return question.render(name, '')


@register.simple_tag
def creedate(qid, *args, **kwargs):
    an = ''
    mois = ''
    jour = ''

    name = "q" + str(qid)
    day, month, year = fait_select_date(name, name, 2000, 2024)
    # name=q69_year, id=row...
    return year.render(name + '_year', an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


@register.simple_tag
def creedob(qid, *args, **kwargs):
    an = ''
    mois = ''
    jour = ''

    name = qid
    day, month, year = fait_select_date(name, name, 1920, 2005)
    # name=q69_year, id=row...
    return year.render(name + '_year', an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)

@register.simple_tag
def creelistepajsm(qid, *args, **kwargs):
    name = "q" + str(qid)
    assistant = kwargs['uid']
    liste1 = Paj.objects.filter(user_id=assistant)
    listevaleurs1 = set()
    for item in liste1:
        listevaleurs1.add(item.paj)
    listevaleurs = Pajsmlist.objects.filter(id__in=listevaleurs1)
    liste = fait_liste_tables(listevaleurs, 'autre')
    question = forms.Select(choices=liste, attrs={'id': name, 'name': name,})
    #   return question.render(name, defaultvalue)
    return question.render(name,'')
