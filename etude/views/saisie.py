import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.db.models import Q, Count
from django.shortcuts import render, redirect
from etude.models import Personne, Questionnaire, Resultatrepetpajsm, Questionpajsm, Resultatpajsm, Accompagnement, Pajsmlist
from accueil.models import Paj

@login_required(login_url=settings.LOGIN_URI)
def select_personne(request):
    # Pour selectionner personne (en fonction de la province), questionnaire
    liste1 = Paj.objects.filter(user_id=request.user)
    listevaleurs = Pajsmlist.objects.filter(id__in=liste1)
    personnes = Personne.objects.filter(selectedpaj_id__in=listevaleurs)
    if request.method == 'POST':
        if request.POST.get('questionnaireid') == '' or request.POST.get('personneid') == '':
            messages.add_message(request, messages.ERROR, 'You have forgotten to chose at least one field')
            return render(
                request,
                'choix.html',
                {
                'personnes': personnes,
                'questionnaires': Questionnaire.objects.all(),
                'accompagnements': Accompagnement.objects.all()
                }
                )

        if 'Choisir1' in request.POST:
            #   pour le NON repetitif
            return redirect(
                            savepajsm,
                            request.POST.get('questionnaireid'),
                            request.POST.get('personneid'),
                            request.POST.get('accompagnementid'),
                            )

        elif 'Repetitif' in request.POST:
            # pour le REPETITIF
            return redirect(saverepetpajsm,
                                request.POST.get('questionnaireid'),
                                request.POST.get('personneid'),
                                )
        elif 'Creer' in request.POST:
            return redirect(creerdossierpajsm)
        elif 'Fermer' in request.POST:
            # pour fermer un dossier
            pid = request.POST.get('personneid')
            personne2 = Personne.objects.get(pk=pid)
            if Personne.objects.filter(pk=pid, assistant=request.user).exists():
                personne = Personne.objects.get(pk=pid, assistant=request.user)
                personne.completed = 1
                personne.save()
                messages.add_message(request, messages.WARNING, personne.code + ' has been closed')
            else:
                messages.add_message(request, messages.ERROR, personne2.code + ' You are not allowed to close this file as you didn''t create it')
            return render(
                    request,
                    'choix.html',
                    {
                        'personnes': personnes,
                        'questionnaires': Questionnaire.objects.all(),
                        'accompagnements': Accompagnement.objects.all(),
                        'message': 'welcome'
                    }
                )
    else:
        return render(
                    request,
                    'choix.html',
                    {
                        'personnes': personnes,
                        'questionnaires': Questionnaire.objects.all(),
                        'accompagnements': Accompagnement.objects.all(),
                        'message': 'welcome'
                    }
                )


@login_required(login_url=settings.LOGIN_URI)
def creerdossierpajsm(request):
    qid = 1
    questionstoutes = Questionpajsm.objects.filter(questionnaire__id=qid)
    if request.method == 'POST':
        reponses = {}
        for question in questionstoutes:
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE':
                an = request.POST.get('q{}_year'.format(question.id))
                if an != "":
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}-{}-{}".format(an, mois, jour)
                else:
                    reponseaquestion = ''
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'CODESTRING':
                    reponseaquestion = encode_donnee(reponseaquestion)
                reponses[question.varname] = reponseaquestion
        selectpajsm = Pajsmlist.objects.get(id=reponses['selectedpaj'])
        pref = 100 * selectpajsm.id
        dernier = Personne.objects.all().order_by('-id').first()
        if dernier is None:
            code = pref + 1
        else:
            code = pref + dernier.id + 1
        reponses['personne_code'] = "{}-{}".format(str(selectpajsm.id), str(code))
        Personne.objects.create(
                                code=reponses['personne_code'],
                                selectedpaj=selectpajsm,
                                date_indexh=reponses['DATEINDEX'],
                                assistant_id=request.user.id
                                )
        textefin = "{} has been created".format(reponses['personne_code'])
        messages.add_message(request, messages.ERROR, textefin)
        return redirect(select_personne)
    else:
        return render(
                    request,
                    'createpajsm.html',
                    {'questions': questionstoutes}
                )


@login_required(login_url=settings.LOGIN_URI)
def savepajsm(request, qid, pid, accid):
    #   genere le questionnaire demande NON repetitif
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = Personne.objects.get(id=pid).code
    questionnaire = Questionnaire.objects.get(id=qid).nom_en
    accompagnement = Accompagnement.objects.get(pk=accid)

    if request.method == 'POST':
        for question in questionstoutes:
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE' or \
                            question.typequestion.nom == 'DATEH':
                reponseaquestion = ''
                an = request.POST.get('q{}_year'.format(question.id))
                if an:
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}-{}-{}".format(an, mois, jour)
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'CODESTRING':
                    reponseaquestion = encode_donnee(reponseaquestion)
                    personne = Personne.objects.get(pk=pid)
                    if personne.__dict__[question.varname] is None:
                        personne.__dict__[question.varname] = reponseaquestion
                        personne.assistant = request.user
                        personne.save()
                else:
                    if not Resultatpajsm.objects.filter(personne_id=pid, question=question, assistant=request.user,
                                                       reponsetexte=reponseaquestion, accompagnement_id=accompagnement.id).exists():
                        Resultatpajsm.objects.update_or_create(personne_id=pid, question=question, assistant=request.user, accompagnement_id=accompagnement.id,
                                # update these fields, or create a new object with these values
                                defaults={
                                    'reponsetexte': reponseaquestion,
                                }
                            )
        now = datetime.datetime.now().strftime('%H:%M:%S')
        messages.add_message(request, messages.WARNING, 'Data saved at ' + now)

    return render(request,
                  'savepajsm.html',
                  {
                      'qid': qid,
                      'pid': pid,
                      'questions': questionstoutes,
                      'ascendancesM': ascendancesM,
                      'ascendancesF': ascendancesF,
                      'code': nomcode,
                      'questionnaire': questionnaire,
                      'accid': accid,
                      'accompagnement': accompagnement
                  }
                )


@login_required(login_url=settings.LOGIN_URI)
def saverepetpajsm(request, qid, pid, accid):
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = Personne.objects.get(id=pid).code
    questionnaire = Questionnaire.objects.get(id=qid).nom_en
    accompagnement = Accompagnement.objects.get(pk=accid)

    if request.method == 'POST':
        actions = request.POST.keys()
        for action in actions:
            if action.startswith('remove_'):
                x = action[len('remove_'):]
                Resultatrepetpajsm.objects.filter(personne__id=pid, assistant=request.user, questionnaire__id=qid, accompagnement__id=accid,
                                                 fiche=x).delete()
                messages.add_message(request, messages.ERROR, 'Card # ' + str(x) + ' removed')
                continue
            elif action.startswith('current_') or action.startswith('add_'):
                if action.startswith('current_'):
                    x = action[len('current_'):]
                else:
                    x = action[len('add_'):]
                    enregistrement = Resultatrepetpajsm.objects.filter(
                                        personne__id=pid,
                                        assistant=request.user,
                                        questionnaire__id=qid,
                                        accompagnement__id=accid).order_by('-fiche').first()
                    ordre = enregistrement.fiche + 1
                    Resultatrepetpajsm.objects.create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                accompagnement_id = accid,
                                question_id=1,
                                fiche=ordre,
                                reponsetexte=10000
                            )
                    messages.add_message(request, messages.WARNING, '1 Fiche ajoutee ')

                for question in questionstoutes:
                    if question.typequestion_id == 5 or question.typequestion_id == 60:
                        an = request.POST.get('q{}Z_Z{}_year'.format(question.id, x))
                        if an != "":
                            mois = request.POST.get('q{}Z_Z{}_month'.format(question.id, x))
                            jour = request.POST.get('q{}Z_Z{}_day'.format(question.id, x))
                            reponseaquestion = "{}-{}-{}".format(an, mois, jour)
                        else:
                            reponseaquestion = ''
                    else:
                        reponseaquestion = request.POST.get('q{}Z_Z{}'.format(question.id, x))
                    if reponseaquestion:
                        if not Resultatrepetpajsm.objects.filter(personne_id=pid,
                                                                assistant_id=request.user.id,
                                                                questionnaire_id=qid,
                                                                question_id=question.id,
                                                                 accompagnement_id=accid,
                                                                fiche=x,
                                                                reponsetexte=reponseaquestion).exists():
                            Resultatrepetpajsm.objects.update_or_create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                question_id=question.id,
                                accompagnement_id=accid,
                                fiche=x,
                                # update these fields, or create a new object with these values
                                defaults={
                                    'reponsetexte': reponseaquestion,
                                }
                            )
                now = datetime.datetime.now().strftime('%H:%M:%S')
                messages.add_message(request, messages.WARNING, 'Donnees enregistrees a ' + now)
    else:
        if Resultatrepetpajsm.objects.filter(personne_id=pid, assistant_id=request.user.id, questionnaire_id=qid, accompagnement__id=accid).count() == 0:
            Resultatrepetpajsm.objects.create(
                                personne_id=pid,
                                assistant_id=request.user.id,
                                questionnaire_id=qid,
                                accompagnement_id = accid,
                                question_id=1,
                                fiche=1,
                                reponsetexte=10000
                            )
    compte, fiches = fait_pagination(pid, qid, accid, request)
    return render(request,
                      'saverepetpajsm.html',
                      {
                          'qid': qid,
                          'pid': pid,
                          'questions': questionstoutes,
                          'ascendancesM': ascendancesM,
                          'ascendancesF': ascendancesF,
                          'fiches': fiches,
                          'compte': compte,
                          'code': nomcode,
                          'questionnaire': questionnaire,
                          'accid': accid,
                          'accompagnement' : accompagnement,
                      }
                  )


def fait_pagination(pid, qid, accid, request):
    donnees = Resultatrepetpajsm.objects.order_by('fiche').filter(
                        personne__id=pid, assistant__id=request.user.id, questionnaire__id=qid, accompagnement__id=accid
                        ).values_list('fiche', flat=True).distinct()
    #donnees = fiche_list.values_list('fiche', flat=True).distinct()
    compte = donnees.count()
    paginator = Paginator(donnees, 3)  # Show 3 fiches par page
    page = request.GET.get('page')
    try:
        fiches = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fiches = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fiches = paginator.page(paginator.num_pages)
    return compte, fiches


def genere_questions(qid):
    questionstoutes = Questionpajsm.objects.filter(questionnaire__id=qid)
    enfants = questionstoutes.select_related('typequestion', 'parent').filter(questionpajsm__parent__id__gt=1)
    ascendancesM = {rquestion.id for rquestion in questionstoutes.select_related('typequestion').filter(pk__in=enfants)}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in questionstoutes.select_related('typequestion').filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)
    return ascendancesF, ascendancesM, questionstoutes


def encode_donnee(message):
    ##PK_path = settings.PUBLIC_KEY_PATH
    ##PK_name = settings.PUBLIC_KEY_NTP2
    ##e = Encrypter()
    #   public_key = e.read_key(PK_path + 'Manitoba_public.pem')
    ##public_key = e.read_key(PK_path + PK_name)
    ##return e.encrypt(message,public_key)
    return message



