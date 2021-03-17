from django.urls import path
from .views import select_personne, saverepetpajsm, savepajsm, creerdossierpajsm, accord_intervenant, \
    inscription_intervenant, suite_accord, saveenquete
from django.contrib.auth.views import LoginView


urlpatterns = [
    #path('login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    #path('', select_personne, name='SelectPersonne'),
    path('', inscription_intervenant, name='inscription'),
    path('saverepetpajsm/<int:qid>/<int:pid>/<int:accid>/', saverepetpajsm, name='saverepetpajsm'),
    path('savepajsm/<int:qid>/<int:pid>/<int:accid>/', savepajsm, name='savepajsm'),
    path('newpajsm/', creerdossierpajsm, name='creerdossierpajsm'),
    path('enquetepaj/', inscription_intervenant, name='inscription_intervenant'),
    path('enquetepaj/<str:iid>', accord_intervenant, name='accord_intervenant'),
    path('accord/<str:iid>', suite_accord, name='suite_accord'),
    path('saveenquetepaj/<str:cid>/<int:qid>', saveenquete, name='saveenquete'),
]