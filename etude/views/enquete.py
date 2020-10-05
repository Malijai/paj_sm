import datetime
import random
import hashlib
from django.contrib import messages
# from django.db.models import Q, Count
from django.shortcuts import render, redirect
from etude.models import Questionnaire, Intervenant, Resultatenquete, Vignette
from .saisie import genere_questions
from django.utils.translation import ugettext_lazy as _
from django.core import mail
from django.conf import settings


# langue = translation.get_language()
#
# if langue == 'fr':
#     CHOIX = CHOIXFR
#     EXPLICATIONS = EXPLICATIONSFR
# else:
#     CHOIX = CHOIXEN
#     EXPLICATIONS = EXPLICATIONSEN


def inscription_intervenant(request):
    # Pour les cas ou les personnes rentrent une adresse de courriel et n'ont pas le lien:
    # Vérifie si la personne existe, et l'état d'avancement du questionnaire
    # Si n'existe pas crée une entrée et envoie un courriel avec le lien
    if request.method == 'POST':
        courriel = request.POST.get('courriel')
        codemd5 = hashlib.md5(courriel.encode())
        code = codemd5.hexdigest()
        #code = 'A' + str(hash(courriel))
        if Intervenant.objects.filter(code=code).exists():
            intervenant = Intervenant.objects.get(code=code)
            if intervenant.completed == 1:
                message = _(u"Ce questionnaire n'est plus disponible pour la personne ayant cette adresse de courriel.")
                messages.add_message(request, messages.WARNING, message)
                return render(request, 'rejet.html')
            elif intervenant.concented == 2:
                message = _(u"2Ce questionnaire n'est plus disponible pour la personne ayant cette adresse de courriel.")
                messages.add_message(request, messages.WARNING, message)
                return render(request, 'rejet.html')
            else:
                lienenquete = settings.ENTREE_URL + intervenant.code
                sujet = _(u"Lien pour l'enquête PAJ-SM")
                textecourriel = _(u"""
                Voici le lien qui vous permettra d'accéder au questionnaire de l'enquête PAJ_SM : {}
                Ne répondez pas à ce courriel, il s'agit d'un envoi automatisé.
                Malijaï Caulet (malijai.caulet.ippm@ssss.gouv.qc.ca)
                    """).format(lienenquete)
                message = _(u"Un message avec le lien pour participer vous a été envoyé à l'adresse suivante : " + intervenant.courriel)
                envoi_courriel(sujet, textecourriel, intervenant.courriel)
                messages.add_message(request, messages.WARNING, message)
                return render(request, 'rejet.html')
        else:
            #code = 'A' + str(hash(courriel))
            codemd5 = hashlib.md5(courriel.encode())
            code = codemd5.hexdigest()
            intervenant = Intervenant.objects.create(
                    courriel=courriel,
                    code=code
                )
            lienenquete = settings.ENTREE_URL + code
            sujet = _(u"Lien pour l'enquête PAJ-SM")
            textecourriel = _(u"""
            Bonjour,
            Voici le lien qui vous permettra d'accéder au questionnaire de l'enquête PAJ_SM : {}
            Si vous n'avez pas le temps de compléter le questionnaire en une séance, vous pourrez retournez où vous étiez en cliquant sur ce même lien.
            Ne répondez pas à ce courriel, il s'agit d'un envoi automatisé.
            Malijaï Caulet (malijai.caulet.ippm@ssss.gouv.qc.ca)
                """).format(lienenquete)
            message = _(u"Un message avec le lien pour participer vous a été envoyé à l'adresse suivante : " + intervenant.courriel)
            envoi_courriel(sujet, textecourriel, intervenant.courriel)
            message = _(u"Un message avec le lien pour participer vous a été envoyé à l'adresse suivante : " + intervenant.courriel)
            messages.add_message(request, messages.WARNING, message)
            return render(request, 'rejet.html', {'courriel': intervenant.courriel,'code': intervenant.code})

    return render(request, 'inscription.html')


def accord_intervenant(request, iid):
    if Intervenant.objects.filter(code=iid).exists():
        intervenant = Intervenant.objects.get(code=iid)
        if intervenant.concented == 1 and intervenant.completed == 0:
            if int(intervenant.partie1) == 0:
                return redirect(saveenquete,
                                intervenant.code,
                                101
                                )
            else:# Continuer en fonction de ce qui est enregistre
                # clef: ordre, connait, implique, avocat,(p1,p2,p3,p4,p5
                #Suivantfait original
                # suivantfait = {(1, 1, 1, 0, (1, 0, 0, 0, 0)): 102,
                #                 (1, 1, 1, 0, (1, 1, 0, 0, 0)): 103,
                #                 (1, 1, 1, 0, (1, 1, 1, 0, 0)): 104,
                #                 (1, 1, 1, 0, (1, 1, 1, 1, 0)): 105,
                #                 (1, 1, 0, 0, (1, 0, 0, 0, 0)): 102,
                #                 (1, 1, 0, 0, (1, 1, 0, 0, 0)): 104,
                #                 (1, 1, 0, 0, (1, 1, 0, 1, 0)): 105,
                #                 (1, 0, 0, 0, (1, 0, 0, 0, 0)): 104,
                #                 (1, 0, 0, 0, (1, 0, 0, 1, 0)): 105,
                #                 (1, 1, 1, 1, (1, 0, 0, 0, 0)): 102,
                #                 (1, 1, 1, 1, (1, 1, 0, 0, 0)): 103,
                #                 (1, 1, 1, 1, (1, 1, 1, 0, 0)): 104,
                #                 (1, 1, 1, 1, (1, 1, 1, 1, 0)): 105,
                #                 (1, 1, 1, 1, (1, 1, 1, 1, 1)): 106,
                #                 (1, 1, 0, 1, (1, 0, 0, 0, 0)): 102,
                #                 (1, 1, 0, 1, (1, 1, 0, 0, 0)): 104,
                #                 (1, 1, 0, 1, (1, 1, 0, 1, 0)): 105,
                #                 (1, 1, 0, 1, (1, 1, 0, 1, 1)): 106,
                #                 (1, 0, 0, 1, (1, 0, 0, 0, 0)): 104,
                #                 (1, 0, 0, 1, (1, 0, 0, 1, 0)): 105,
                #                 (1, 0, 0, 1, (1, 0, 0, 1, 1)): 106,
                #                 (2, 1, 1, 0, (1, 0, 0, 0, 0)): 105,
                #                 (2, 1, 1, 0, (1, 0, 0, 0, 1)): 102,
                #                 (2, 1, 1, 0, (1, 1, 0, 0, 1)): 103,
                #                 (2, 1, 1, 0, (1, 1, 1, 0, 1)): 104,
                #                 (2, 1, 0, 0, (1, 0, 0, 0, 0)): 105,
                #                 (2, 1, 0, 0, (1, 0, 0, 0, 1)): 102,
                #                 (2, 1, 0, 0, (1, 1, 0, 0, 1)): 104,
                #                 (2, 0, 0, 0, (1, 0, 0, 0, 0)): 105,
                #                 (2, 0, 0, 0, (1, 0, 0, 0, 1)): 104,
                #                 (2, 1, 1, 1, (1, 0, 0, 0, 0)): 105,
                #                 (2, 1, 1, 1, (1, 0, 0, 0, 1)): 102,
                #                 (2, 1, 1, 1, (1, 1, 0, 0, 1)): 103,
                #                 (2, 1, 1, 1, (1, 1, 1, 0, 1)): 104,
                #                 (2, 1, 1, 1, (1, 1, 1, 1, 1)): 106,
                #                 (2, 1, 0, 1, (1, 0, 0, 0, 0)): 105,
                #                 (2, 1, 0, 1, (1, 0, 0, 0, 1)): 102,
                #                 (2, 1, 0, 1, (1, 1, 0, 0, 1)): 104,
                #                 (2, 1, 0, 1, (1, 1, 0, 1, 1)): 106,
                #                 (2, 0, 0, 1, (1, 0, 0, 0, 0)): 105,
                #                 (2, 0, 0, 1, (1, 0, 0, 0, 1)): 104,
                #                 (2, 0, 0, 1, (1, 0, 0, 1, 1)): 106,
                #         }
                #Suivantfait étudiants (pas de partie3)
                # clef: ordre, connait, implique, avocat,(p1,p2,p3,p4,p5
                suivantfait = {(1, 1, 1, 0, (1, 0, 0, 0, 0)): 102,
                               (1, 1, 1, 0, (1, 1, 0, 0, 0)): 104,
                               #(1, 1, 1, 0, (1, 1, 1, 0, 0)): 104,
                               (1, 1, 1, 0, (1, 1, 0, 1, 0)): 105,
                               (1, 1, 0, 0, (1, 0, 0, 0, 0)): 102,
                               (1, 1, 0, 0, (1, 1, 0, 0, 0)): 104,
                               (1, 1, 0, 0, (1, 1, 0, 1, 0)): 105,
                               (1, 0, 0, 0, (1, 0, 0, 0, 0)): 104,
                               (1, 0, 0, 0, (1, 0, 0, 1, 0)): 105,
                               (1, 1, 1, 1, (1, 0, 0, 0, 0)): 102,
                               (1, 1, 1, 1, (1, 1, 0, 0, 0)): 104,
                               #(1, 1, 1, 1, (1, 1, 1, 0, 0)): 104,
                               (1, 1, 1, 1, (1, 1, 0, 1, 0)): 105,
                               (1, 1, 1, 1, (1, 1, 0, 1, 1)): 106,
                               (1, 1, 0, 1, (1, 0, 0, 0, 0)): 102,
                               (1, 1, 0, 1, (1, 1, 0, 0, 0)): 104,
                               (1, 1, 0, 1, (1, 1, 0, 1, 0)): 105,
                               (1, 1, 0, 1, (1, 1, 0, 1, 1)): 106,
                               (1, 0, 0, 1, (1, 0, 0, 0, 0)): 104,
                               (1, 0, 0, 1, (1, 0, 0, 1, 0)): 105,
                               (1, 0, 0, 1, (1, 0, 0, 1, 1)): 106,
                               (2, 1, 1, 0, (1, 0, 0, 0, 0)): 105,
                               (2, 1, 1, 0, (1, 0, 0, 0, 1)): 102,
                               (2, 1, 1, 0, (1, 1, 0, 0, 1)): 104,
                               #(2, 1, 1, 0, (1, 1, 1, 0, 1)): 104,
                               (2, 1, 0, 0, (1, 0, 0, 0, 0)): 105,
                               (2, 1, 0, 0, (1, 0, 0, 0, 1)): 102,
                               (2, 1, 0, 0, (1, 1, 0, 0, 1)): 104,
                               (2, 0, 0, 0, (1, 0, 0, 0, 0)): 105,
                               (2, 0, 0, 0, (1, 0, 0, 0, 1)): 104,
                               (2, 1, 1, 1, (1, 0, 0, 0, 0)): 105,
                               (2, 1, 1, 1, (1, 0, 0, 0, 1)): 102,
                               (2, 1, 1, 1, (1, 1, 0, 0, 1)): 104,
                               #(2, 1, 1, 1, (1, 1, 1, 0, 1)): 104,
                               (2, 1, 1, 1, (1, 1, 0, 1, 1)): 106,
                               (2, 1, 0, 1, (1, 0, 0, 0, 0)): 105,
                               (2, 1, 0, 1, (1, 0, 0, 0, 1)): 102,
                               (2, 1, 0, 1, (1, 1, 0, 0, 1)): 104,
                               (2, 1, 0, 1, (1, 1, 0, 1, 1)): 106,
                               (2, 0, 0, 1, (1, 0, 0, 0, 0)): 105,
                               (2, 0, 0, 1, (1, 0, 0, 0, 1)): 104,
                               (2, 0, 0, 1, (1, 0, 0, 1, 1)): 106,
                               }
                qid = suivantfait[intervenant.ordre, intervenant.connait, intervenant.implique, intervenant.avocat,
                                  (int(intervenant.partie1), int(intervenant.partie2), int(intervenant.partie3),
                                  int(intervenant.partie4), int(intervenant.partie5))]
                return redirect(saveenquete,
                                intervenant.code,
                                qid,
                                )
        elif intervenant.concented == 1 and intervenant.completed == 1:
            messages.add_message(request, messages.ERROR, _(u'Vous avez déjà répondu a toutes les questions de cette enquete. Merci !'))
            return render(request, 'rejet.html')
        elif intervenant.concented == 0:
        # Proceder au consentement
            return suite_accord(request, intervenant.code)
        elif intervenant.concented == 2:
            messages.add_message(request, messages.ERROR, _(u'Vous avez déjà refusé de participer à cette enquete !'))
            return render(request, 'rejet.html')
    else:
        return redirect('inscription_intervenant')


def suite_accord(request, iid):
    intervenant = Intervenant.objects.get(code=iid)
    # Intervenant reconnu doit consentir a participer.
    # L ordre et les vignettes sont assignees a ce moment la
    if request.method == 'POST':
        actions = request.POST.keys()
        for action in actions:
            if action.startswith('Consent'):
                ordre = random.randint(1, 2)
                vignette1 = random.randint(1, 16)
                vignette2 = random.randint(17, 32)
                intervenant.concented = 1
                intervenant.ordre = ordre
                intervenant.vignette1 = vignette1
                intervenant.vignette2 = vignette2
                intervenant.date_consentement = datetime.datetime.now()
                intervenant.save()
                messages.add_message(request, messages.ERROR, _(u'Merci pour votre consentement à participer'))
                return redirect(saveenquete,
                                intervenant.code,
                                101,
                                )
            elif action.startswith('Refuser'):
                intervenant.concented = 2
                intervenant.courriel = "refus"
                intervenant.save()
                messages.add_message(request, messages.ERROR, _(u'Merci. Votre refus de participer est enregistré !'))
                return render(request, 'rejet.html')

    return render(request, 'accord.html', {'intervenant': intervenant})


def saveenquete(request, cid, qid):
    # genere le questionnaire en fonction de l<ordre, de la reponse a certaines questions
    # et des vignettes tirees au sort
    # print(' qid recu - ', qid, ' - ')
    complete = {
        101: 'partie1',
        102: 'partie2',
        103: 'partie3',
        105: 'partie5',
        106: 'partie6',
        104: 'partie4',
    }
    condition = {
        'CN28': 'implique',
        'ID8': 'connait',
        'ID7': 'avocat',
    }
    #clef: ordre, connait, implique, avocat (sont les seuls qui font le 106)
    #1 0 1 0
    # Suivant original
    # suivant = {(1, 1, 1, 0): {101: 102, 102: 103, 103: 104, 104: 105, 105: 110},
    #            (1, 1, 0, 0): {101: 102, 102: 104, 104: 105, 105: 110},
    #            (1, 0, 0, 0): {101: 104, 104: 105, 105: 110},
    #            (1, 1, 1, 1): {101: 102, 102: 103, 103: 104, 104: 105, 105: 106, 106: 110},
    #            (1, 1, 0, 1): {101: 102, 102: 104, 104: 105, 105: 106, 106: 110},
    #            (1, 0, 0, 1): {101: 104, 104: 105, 105: 106, 106: 110},
    #            (2, 1, 1, 0): {101: 105, 105: 102, 102: 103, 103: 104, 104: 110},
    #            (2, 1, 0, 0): {101: 105, 105: 102, 102: 104, 104: 110},
    #            (2, 0, 0, 0): {101: 105, 105: 104, 104: 110},
    #            (2, 1, 1, 1): {101: 105, 105: 102, 102: 103, 103: 104, 104: 106, 106: 110},
    #            (2, 1, 0, 1): {101: 105, 105: 102, 102: 104, 104: 106, 106: 110},
    #            (2, 0, 0, 1): {101: 105, 105: 104, 104: 106, 106: 110},
    #            }
    # Suivant etudiants (pas de 103)
    suivant = {(1, 1, 1, 0): {101: 102, 102: 104, 104: 105, 105: 110},
               (1, 1, 0, 0): {101: 102, 102: 104, 104: 105, 105: 110},
               (1, 0, 0, 0): {101: 104, 104: 105, 105: 110},
               (1, 1, 1, 1): {101: 102, 102: 104, 104: 105, 105: 106, 106: 110},
               (1, 1, 0, 1): {101: 102, 102: 104, 104: 105, 105: 106, 106: 110},
               (1, 0, 0, 1): {101: 104, 104: 105, 105: 106, 106: 110},
               (2, 1, 1, 0): {101: 105, 105: 102, 102: 104, 104: 110},
               (2, 1, 0, 0): {101: 105, 105: 102, 102: 104, 104: 110},
               (2, 0, 0, 0): {101: 105, 105: 104, 104: 110},
               (2, 1, 1, 1): {101: 105, 105: 102, 102: 104, 104: 106, 106: 110},
               (2, 1, 0, 1): {101: 105, 105: 102, 102: 104, 104: 106, 106: 110},
               (2, 0, 0, 1): {101: 105, 105: 104, 104: 106, 106: 110},
               }
    intervenant = Intervenant.objects.get(code=cid)
    vignette1 = Vignette.objects.get(id= intervenant.vignette1)
    vignette2 = Vignette.objects.get(id= intervenant.vignette2)
    questionnaire = Questionnaire.objects.get(id=qid)
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    if request.method == 'POST':
        if 'suite' in request.POST and qid != 110:
            for question in questionstoutes:
                if question.typequestion.nom == 'DUREE':
                    an = request.POST.get('q{}_year'.format(question.id))
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}ans-{}mois-{}jours".format(an, mois, jour)
                else:
                    reponseaquestion = request.POST.get('q' + str(question.id))
                # print(question.id, ' - ', question.varname, ' + ', reponseaquestion)
                if reponseaquestion:
                    if not Resultatenquete.objects.filter(intervenant_id=intervenant.id, question=question,
                                                          reponsetexte=reponseaquestion).exists():
                        Resultatenquete.objects.update_or_create(intervenant_id=intervenant.id, questionnaire=questionnaire, question=question,
                            defaults={
                                'reponsetexte': reponseaquestion,
                                }
                            )
                    if question.varname in condition.keys():
                        if int(reponseaquestion) == 1:
                            reponse = 1
                        else:
                            reponse = 0
                        intervenant.__dict__[condition[question.varname]] = reponse
                        intervenant.save()
            now = datetime.datetime.now().strftime('%H:%M:%S')
            old_qid = int(request.POST.get('qid'))
            new_qid = old_qid
            if (intervenant.ordre, intervenant.connait, intervenant.implique, intervenant.avocat) in suivant:
                messages.add_message(request, messages.WARNING, _(u'Enregistre a ' + now))
                intervenant.__dict__[complete[old_qid]] = 1
                intervenant.save()
                new_qid = suivant[(intervenant.ordre, intervenant.connait, intervenant.implique, intervenant.avocat)][old_qid]
#                ascendancesF, ascendancesM, questionstoutes = genere_questions(new_qid)
#                questionnaire = Questionnaire.objects.get(id=new_qid)
                qid = new_qid
            else:
                messages.add_message(request, messages.ERROR, _(u'Certaines de vos réponses sont incompatibles, s il vous plait recommencez !'))
            if new_qid == 110:
                intervenant.completed = 1
                intervenant.courriel = "termine"
                intervenant.save()
                messages.add_message(request, messages.ERROR,
                                     _(u'Questionnaire terminé, Merci !'))
                return render(request, 'rejet.html')
            return redirect(saveenquete,
                            cid,
                            qid,
                            )
        elif qid == 110:
            messages.add_message(request, messages.ERROR,
                                 _(u'Vous avez déjà répondu a toutes les questions de cette enquete, Merci !'))
            return render(request, 'rejet.html')
    else:
        # print('qid - ', qid, ' - ')
        return render(request, 'saveenquete.html',
                                 {
                                   'qid': qid,
                                   'questions': questionstoutes,
                                   'ascendancesM': ascendancesM,
                                   'ascendancesF': ascendancesF,
                                   'questionnaire': questionnaire,
                                   'intervenant': intervenant,
                                   'range': range(1, int(questionnaire.description)+1),
                                   'vignette1': vignette1,
                                   'vignette2': vignette2,
                                 }
                             )


def envoi_courriel(sujet, textecourriel, courriel):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            sujet, textecourriel, 'malijai.caulet@ntp-ptn.org', [courriel],
            connection=connection,
        ).send()