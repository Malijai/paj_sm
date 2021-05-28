from __future__ import unicode_literals
from django import template
import re
from django.apps import apps
from etude.models import Reponsepajsm, Vignette
from etude.etude_constants import CHOIX_ON, CHOIX_ONUK, CHOIX_ONNSP, CHOIX_VFNSP, CHOIX_MOINSPLUS, CHOIX_UNDIX, \
    CHOIX_UNCINQ, CHOIX_UNSIX, CHOIX_UNCINQ2

register = template.Library()


@register.simple_tag
def spss_pajinter_dichou(type, stats, *args, **kwargs):
    if type == "DICHO":
        liste = CHOIX_ON.items()
    elif type == "ONNSP":
        liste = CHOIX_ONNSP.items()
    elif type == "ONNSP":
        liste = CHOIX_ONNSP.items()
    elif type == "MOINSPLUS":
        liste = CHOIX_MOINSPLUS.items()
    elif type == "UNDIX":
        liste = CHOIX_UNDIX.items()
    elif type == "UNCINQ":
        liste = CHOIX_UNCINQ.items()
    elif type == "UNCINQ2":
        liste = CHOIX_UNCINQ2.items()
    elif type == "UNSIX":
        liste = CHOIX_UNSIX.items()
    elif type == "VRAIFAUX":
        liste = CHOIX_VFNSP.items()
    elif type == "DICHOU":
        liste = CHOIX_ONUK.items()

    return fait_pajinter_rendu(liste, stats)


@register.simple_tag
def spss_pajinter_reponse(qid, stats, *args, **kwargs):
    #Pour listes de valeurs specifiques a chaque question
    listevaleurs = Reponsepajsm.objects.filter(question_id=qid, )
    liste = []
    for valeur in listevaleurs:
        val = valeur.reponse_valeur
        nen = valeur.reponse_en
        liste.append((val, nen))
    return fait_pajinter_rendu(liste, stats)


@register.simple_tag
def fait_pajinter_rendu(liste, stats):
    sortie = ''
    if stats == 'stata':
        nb = len(liste)
        for i, val in enumerate(liste, 1):
            sortie += '{} "{}"  '. format(val[0], val[1])
            if i == nb:
                sortie += "\n"
    elif stats == 'spss':
        nb = len(liste)
        for i, val in enumerate(liste, 1):
            sortie += '{}        "{}"'. format(val[0], val[1])
            if i == nb:
                sortie += "/\n."
            else:
                sortie += "\n"
    elif stats == 'R':
        nb = len(liste)
        for i, val in enumerate(liste, 1):
            sortie += '{}  {}'.format(val[0], val[1])
            if i == nb:
                sortie += "\n\")"
            else:
                sortie += "\n"
    else:
        nb = len(liste)
        sortie += '= {\n'
        for i, val in enumerate(liste, 1):
            sortie += '{} : "{}"'. format(val[0], val[1])
            if i == nb:
                sortie += "}\n"
            else:
                sortie += ",\n "
    return sortie


@register.simple_tag
def fait_pajinter_vignettes(type, stats):
    sortie = ''
    i = 0
    if type == 1:
        liste = Vignette.objects.filter(id__lt=17)
    else:
        liste = Vignette.objects.filter(id__gt=16)
    nb = len(liste)
    for item in liste:
        sortie += '{}  {}'.format(item.id, item.reponse_valeur)
        i += 1
        if i == nb:
            sortie += "\n\")"
        else:
            sortie += "\n"
    return sortie