from django.urls import include, path
from .views import accueil, entreesystemes


urlpatterns = [
    path('', accueil, name='accueil'),
    path('datas', entreesystemes, name='entreesystemes'),
]
