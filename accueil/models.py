from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

# Create your models here.
class Projet(models.Model):
    Enq = 1
    File = 2
    ALL = 10
    PROJETS_CHOICES = (
                           (Enq, 'Enquete'),
                           (File, 'PAJ- dossiers tribunaux'),
                           (ALL, 'All projects'),
                        )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projet = models.PositiveSmallIntegerField(choices=PROJETS_CHOICES, verbose_name="Projets", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Pajcodes(object):
    p100 = 100
    p1 = 1
    p2 = 2
    p3 = 3
    p4 = 4
    p5 = 5
    p6 = 6
    p7 = 7
    p8 = 8
    p9 = 9
    p10 = 10
    PAJS_CHOICES = (
        (p1, 'PAJ-Montréal'),
        (p2, 'PAJ-Québec'),
        (p3, 'PAJ-St-Jérôme'),
        (p4, 'PAJ-Trois Rivières'),
        (p5, 'PAJ-Joliette'),
        (p6, 'PAJ-Chicoutimi'),
        (p7, 'PAJ-Sherbrooke'),
        (p8, "PAJ-Val d'Or"),
        (p9, 'PAJ-Longueuil'),
        (p10, 'PAJ-Gatineau'),
        (p100, 'Pas de PAJ'),
    )


class Paj(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paj = models.PositiveSmallIntegerField(choices=Pajcodes().PAJS_CHOICES, verbose_name="Paj attribué", null=True, blank=True)

    def __str__(self):
        return self.user.username
