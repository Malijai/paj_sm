from django.urls import include, path
from .views import accueil


urlpatterns = [
    path('', accueil, name='accueil'),

]
