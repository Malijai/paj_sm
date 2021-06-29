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


class Paj(models.Model):
    p100 = 100
    p1 = 1
    p2 = 2
    p3 = 3
    p4 = 4
    PAJS_CHOICES = (
                           (p1, 'PAJ-1'),
                           (p2, 'PAJ-2'),
                           (p3, 'PAJ-3'),
                           (p4, 'PAJ-4'),
                           (p100, 'AucunPAJ'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paj = models.PositiveSmallIntegerField(choices=PAJS_CHOICES, verbose_name="Paj attribué", null=True, blank=True)

    def __str__(self):
        return self.user.username
