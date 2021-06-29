from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
#from etude.views import select_personne
from accueil.models import Projet

def accueil(request):
    return render(request,'indexpaj.html')
    #return redirect('inscription', 1)


@login_required(login_url=settings.LOGIN_URI)
def entreesystemes(request):
    Enq = False
    File = False

    droits = Projet.objects.filter(user_id=request.user.id)

    for droit in droits:
        if droit.projet == Projet.Enq:
            Enq = True
        elif droit.projet == Projet.File:
            File = True
        elif droit.projet == Projet.ALL:
            Enq = True
            File = True

    return render(request, "entreesystemes.html",
                      {
                        'Enq': Enq,
                        'File': File,
                      })