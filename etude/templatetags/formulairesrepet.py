from __future__ import unicode_literals
from django import template
from django.apps import apps
from etude.models import Resultatrepetpajsm, Reponsepajsm, Questionpajsm, Typequestion, Listevaleur, Victime
from django import forms
from .formulairespajsm import fait_select_date, fait_liste_tables, enlevelisttag
from etude.etude_constants import CHOIX_ONUK, CHOIX_ON

register = template.Library()


@register.simple_tag
def fait_table(qid, sorte, *args, **kwargs):
    #questid sorte
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    idcondition = fait_id(qid, cible, relation=relation)

    typeq = Typequestion.objects.get(nom=sorte)
    listevaleurs = Listevaleur.objects.filter(typequestion=typeq)
    name = 'q{}Z_Z{}'.format(qid, ordre)
    if sorte == "VIOLATION":
        liste = fait_liste_tables(listevaleurs, 'violation')
    else:
        liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition, 'name': name})
    return question.render(name, defaultvalue)


@register.simple_tag
def fait_reponse(qid, b, *args, **kwargs):
    #Pour listes de valeurs specifiques a chaque question
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    idcondition = fait_id(qid, cible, relation=relation)

    listevaleurs = Reponsepajsm.objects.filter(question__id=qid, )
    name = 'q{}Z_Z{}'.format(qid, ordre)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition,'name': name, })

#   return question.render(name, defaultvalue)
    return question.render(name, defaultvalue)

@register.simple_tag
def fait_victimes(qid, sorte, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur (independant de la province)
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    idcondition = fait_id(qid, cible, relation=relation)

    listevaleurs = Victime.objects.all()
    name = 'q{}Z_Z{}'.format(qid, ordre)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition,'name': name, })
    return question.render(name, defaultvalue)


@register.simple_tag
def fait_table_valeurs_prov(qid, sorte, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur
    #et dont la liste depend de la province
    province =  kwargs['province']
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    typetable = {"ETABLISSEMENT": "etablissement", "MUNICIPALITE": "municipalite",}
    tableext = typetable[sorte]
    assistant = kwargs['uid']
    ordre = kwargs['ordre']
    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    idcondition = fait_id(qid, cible, relation=relation)

    Klass = apps.get_model('dataentry', tableext)
    # Klass = apps.get_model('dataentry', typetable[b])
    listevaleurs = Klass.objects.filter(province__id=province)
    name = 'q{}Z_Z{}'.format(qid, ordre)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition,'name': name})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_dichou(qid, sorte, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    idcondition = fait_id(qid, cible, relation=relation)
    name = 'q{}Z_Z{}'.format(qid, ordre)
    if sorte == "DICHO":
        liste = CHOIX_ON.items()
        question = forms.RadioSelect(choices=liste, attrs={'id': idcondition, 'name': name})
    else:
        liste = CHOIX_ONUK.items()
        question = forms.RadioSelect(choices=liste, attrs={'id': idcondition, 'name': name})

    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_court(qid, sorte, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    idcondition = fait_id(qid, cible, relation=relation)
    name = 'q{}Z_Z{}'.format(qid, ordre)

    liste = [(1, 'Municipal'), (2, 'Provincial'), (3, 'Superior')]
    question = forms.Select(choices=liste, attrs={'id': idcondition, 'name': name, })

    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_textechar(qid, sorte, persid, relation, cible, uid, ordre, *args, **kwargs):
    personneid = persid
    relation = relation
    cible = cible
    assistant = uid
    ordre = ordre

    defaultvalue = fait_default(personneid, qid, assistant=assistant, ordre=ordre)
    idcondition = fait_id(qid, cible, relation=relation)
    name = 'q{}Z_Z{}'.format(qid, ordre)
    if sorte == 'STRING' or sorte == 'CODESTRING' or sorte == 'TIME':
        question = forms.TextInput(attrs={'size': 30, 'id': idcondition,'name': name,})
    else:
        question = forms.NumberInput(attrs={'size': 30, 'id': idcondition,'name': name,})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_date(qid, b, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    ordre = kwargs['ordre']

    an = ''
    mois = ''
    jour = ''
    if Resultatrepetpajsm.objects.filter(personne__id=personneid, assistant__id=assistant, question__id=qid,fiche=ordre).exists():
        ancienne = Resultatrepetpajsm.objects.get(personne__id=personneid, assistant__id=assistant, question__id=qid,
                                            fiche=ordre).__str__()
        if ancienne:
            an, mois, jour = ancienne.split('-')

    idcondition = fait_id(qid, cible, relation=relation)
    name = 'q{}Z_Z{}'.format(qid, ordre)
    day, month, year = fait_select_date(idcondition, name, 1960, 2024)
# #name=q69_year, id=row...
    return year.render(name + '_year' , an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


def fait_default(personneid, qid, *args, **kwargs):
    ##fail la valeur par deffaut
    assistant = kwargs['assistant']
    ordre = kwargs['ordre']
    ancienne = ''

    if Resultatrepetpajsm.objects.filter(personne__id=personneid, assistant__id=assistant, question__id=qid, fiche=ordre).exists():
        ancienne = Resultatrepetpajsm.objects.get(personne__id=personneid, assistant__id=assistant,
                                                 question__id=qid, fiche=ordre).__str__()

    return ancienne


def fait_id(qid, cible, *args, **kwargs):
    ##fail l'ID pour javascripts ou autre
    relation = kwargs['relation']

    idcondition = ''
    if relation != '' and cible != '':
        idcondition = 'row-{}X{}X{}'.format(qid, relation, cible)
    return idcondition


@register.simple_tag
def fait_dateh(persid, *args, ** kwargs):
    #   Va chercher les dates de sorte 60 pour les afficher dans les tabs
    ordre = kwargs['ordre']
    assistant = kwargs['assistant']
    questionnaire = kwargs['questionnaire']
    accompagnement = kwargs['accompagnement']

    datehosp = ''
    question = Questionpajsm.objects.get(typequestion_id=60, questionnaire_id=questionnaire).pk
    if Resultatrepetpajsm.objects.filter(personne__id=persid, assistant__id=assistant, question_id=question, fiche=ordre,accompagnement_id=accompagnement).exists():
        datehosp = Resultatrepetpajsm.objects.get(personne__id=persid, assistant__id=assistant,
                                                 question__id=question, fiche=ordre,accompagnement_id=accompagnement).__str__()
    else:
        datehosp = ordre
    if questionnaire == 10:
        texte = 'Audience du : '
    else:
        texte = 'Délit #{} du :'.format(ordre)
    return '<h3>{}</h3><b>{} {}</b>'.format(datehosp, texte, datehosp)

