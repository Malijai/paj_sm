from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
#from etude.views import select_personne


def accueil(request):
    return render(request,'indexpaj.html')
    #return redirect('inscription', 1)


#@login_required(login_url=settings.LOGIN_URI)
#def entreesystemes(request):
#    return redirect(select_personne)

