from django.urls import path
from .views import select_personne, saverepetpajsm, savepajsm, creerdossierpajsm, accord_intervenant, \
    inscription_intervenant, suite_accord, saveenquete, bilan_sondage, bilan_etude, prepare_csv, ffait_csv, \
    fait_entete_pajinter_R, fait_entete_pajsaisie_R, ffait_csv_pajsaisie, prepare_csv_pajsaisie,questions_pdf, \
    fait_entete_spss
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    # pour dossiers
    path('pajfile', select_personne, name='SelectPersonne'),
    path('<str:cissid>', inscription_intervenant, name='inscription'),
    path('saverepetpajsm/<int:qid>/<int:pid>/<int:accid>/', saverepetpajsm, name='saverepetpajsm'),
    path('savepajsm/<int:qid>/<int:pid>/<int:accid>/', savepajsm, name='savepajsm'),
    path('newpajsm/', creerdossierpajsm, name='creerdossierpajsm'),
    # pour enquete
    #path('enquetepaj/', inscription_intervenant, name='inscription_intervenant'),
    path('enquetepaj/<str:iid>', accord_intervenant, name='accord_intervenant'),
    path('accord/<str:iid>', suite_accord, name='suite_accord'),
    path('saveenquetepaj/<str:cid>/<int:qid>', saveenquete, name='saveenquete'),
    path('bilan/', bilan_sondage, name='bilan_sondage'),
    path('bilan2/', bilan_etude, name='bilan_etude'),
    path('csv/<int:questionnaire>/<int:tous>/', prepare_csv, name='prepare_csv'),
    path('csvpaj/<int:paj>/<int:questionnaire>/<int:tous>/<int:seuil>', prepare_csv_pajsaisie, name='prepare_csv_pajsaisie'),
    path('csv/<int:questionnaire>/<int:iteration>/<int:seuil>/<int:tous>/', ffait_csv, name='do_csv'),
    path('enteteR/<int:questionnaire>/', fait_entete_pajinter_R, name='fait_entete_pajinter_R'),
    path('enteteRS/<int:questionnaire>/', fait_entete_pajsaisie_R, name='fait_entete_pajsaisie_R'),
    path('csvpaj/<int:paj>/<int:questionnaire>/<int:iteration>/<int:seuil>/<int:tous>/', ffait_csv_pajsaisie,name='ffait_csv_pajsaisie'),
    path('pdf/<int:questionnaire>/', questions_pdf, name='questions_pdf'),
    path('enteteSPSS_S/<int:questionnaire>/', fait_entete_spss, name='fait_entete_spss'),

]