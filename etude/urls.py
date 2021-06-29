from django.urls import path
from .views import select_personne, saverepetpajsm, savepajsm, creerdossierpajsm, accord_intervenant, \
    inscription_intervenant, suite_accord, saveenquete, bilan_sondage, prepare_csv, ffait_csv, fait_entete_pajinter_R
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('pajfile', select_personne, name='SelectPersonne'),
    path('<str:cissid>', inscription_intervenant, name='inscription'),
    path('saverepetpajsm/<int:qid>/<int:pid>/<int:accid>/', saverepetpajsm, name='saverepetpajsm'),
    path('savepajsm/<int:qid>/<int:pid>/<int:accid>/', savepajsm, name='savepajsm'),
    path('newpajsm/', creerdossierpajsm, name='creerdossierpajsm'),
    #path('enquetepaj/', inscription_intervenant, name='inscription_intervenant'),
    path('enquetepaj/<str:iid>', accord_intervenant, name='accord_intervenant'),
    path('accord/<str:iid>', suite_accord, name='suite_accord'),
    path('saveenquetepaj/<str:cid>/<int:qid>', saveenquete, name='saveenquete'),
    path('bilan/', bilan_sondage, name='bilan_sondage'),
    path('csv/<int:questionnaire>/<int:tous>/', prepare_csv, name='prepare_csv'),
    path('csv/<int:questionnaire>/<int:iteration>/<int:seuil>/<int:tous>/', ffait_csv, name='do_csv'),
    path('enteteR/<int:questionnaire>/', fait_entete_pajinter_R, name='fait_entete_pajinter_R'),
]