from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

DEFAULT_UID = 1
# met tous les utilisateurs par defaut a 1 (maliadmin)

## Table des CISSS et CIUSSS (enquete)
class Centresante(models.Model):
    nom = models.CharField(max_length=250, verbose_name="Nom du CISSS ou CIUSSS",)
    lien = models.CharField(max_length=250, verbose_name="Url du commissaire aux plaintes CISSS ou CIUSSS", blank=True, null=True)
    logo = models.ImageField(upload_to='Logos', verbose_name="Logo format png", help_text="PAS D'ACCENT DANS LES NOMS DE FICHIERS", null=True, blank=True)
    courriel = models.CharField(max_length=250, verbose_name="Courriel commissaire aux plaintes")
    tel1 = models.CharField(max_length=250, verbose_name="Tel1 commissaire aux plaintes")
    tel2 = models.CharField(max_length=250, verbose_name="Autre tel du commissaire aux plaintes", blank=True, null=True)

    def __str__(self):
        return '%s' % self.nom


## Table des repondants (intervenants, professionnels etc) (enquete)
### order = ordre des questionnaires (aléatoire), vignettes associées au répondant (aléatoires)
class Intervenant(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Lien : https://pajsmmj.ntp-ptn.org/PAJSM/enquetepaj/")
    courriel = models.CharField(max_length=250)
    completed = models.IntegerField(default=0)
    concented = models.IntegerField(default=0, verbose_name="Consent = 1, Refuse = 2")
    tirage = models.IntegerField(default=0)
    utilisationsecondaire = models.IntegerField(default=0)
    contactfutur = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordre = models.IntegerField(default=0, verbose_name="ordre 1= I, II, III etc; ordre 2= I, V, II etc")
    vignette1 = models.IntegerField(default=0)
    vignette2 = models.IntegerField(default=0)
    date_consentement = models.DateTimeField(blank=True, null=True)
    partie1 = models.IntegerField(default=0, verbose_name="Partie I terminée")
    partie2 = models.IntegerField(default=0, verbose_name="Partie II terminée")
    partie3 = models.IntegerField(default=0, verbose_name="Partie III terminée")
    partie4 = models.IntegerField(default=0, verbose_name="Partie IV terminée")
    partie5 = models.IntegerField(default=0, verbose_name="Partie V terminée")
    partie6 = models.IntegerField(default=0, verbose_name="Partie VI terminée")
    implique = models.IntegerField(default=0)
    connait = models.IntegerField(default=0)
    avocat = models.IntegerField(default=0)
    centresante = models.ForeignKey(Centresante, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (('code', 'courriel',),)
        indexes = [models.Index(fields=['code', 'courriel'])]

    def __str__(self):
        return '%s' % self.code


## listes de valeurs typequestion_id=13 (Paj-sm)
class Pajsmlist(models.Model):
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)

    def __str__(self):
        return '%s' % self.reponse_en


## Table des participants aux PAJSM (étude)
class Personne(models.Model):
    code = models.CharField(max_length=200,)
    selectedpaj = models.ForeignKey(Pajsmlist, default=100, on_delete=models.DO_NOTHING)
    date_indexh = models.DateField(blank=True, null=True)
    completed = models.IntegerField(default=0)
    genre = models.CharField(max_length=200, blank=True, null=True)
    assistant = models.ForeignKey(User, default=DEFAULT_UID, on_delete=models.DO_NOTHING)
    sed = models.TextField(blank=True, null=True)
    nam = models.TextField(blank=True, null=True)
    sddob = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['selectedpaj', 'code']

    def __str__(self):
        return '%s' % self.code


## Definit la forme html des questions ainsi que le type de réponse attendu (texte, bool, date etc)
class Typequestion(models.Model):
    nom = models.CharField(max_length=200, )
    tatable = models.CharField(max_length=200, blank=True, null=True)
    taille = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom


##   listes valeurs non dependantes des provinces SANS province
class Listevaleur(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['typequestion', 'reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_en


class Victime(models.Model):
    #  listes de valeurs typequestion_id=14 (VICTIME)
    #  Restee a part a cause de la logique du tri des items
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.reponse_en


## Accompagnement = suivi par le PAJ_SM (un peut comme verdict ou hearing dans NTP) (étude)
class Accompagnement(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.reponse_en


class Questionnaire(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )
    description = models.CharField(max_length=200, )
    consigneen = models.TextField(blank=True, null=True,)
    consignefr = models.TextField(blank=True, null=True,)

    def __str__(self):
        return '%s' % self.nom_en


#######################
## Questions utilisees pour tous les questionnaires
# Parent_ID permet de lier l'affichage conditionnel d'une question en fonction de la réponse précédente
# à la question dont l'ID=Parent_id via la relation établie par  le champ relation et la valeur cible prédéfinie
# (par exemple question 2 s'ouvrira si question 1 (parent_id) a comme réponse 998 (cible) avec relation égale)
DEFAULT_PARENT_ID = 1


class Questionpajsm(models.Model):
    questionno = models.IntegerField()
    questionen = models.TextField()
    questionfr = models.TextField(blank=True, null=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey("self", default=DEFAULT_PARENT_ID, on_delete=models.DO_NOTHING)
    relation = models.CharField(blank=True, null=True, max_length=45,)
    cible = models.CharField(blank=True, null=True, max_length=45,)
    varname = models.CharField(blank=True, null=True, max_length=45,)
    aidefr = models.TextField(blank=True, null=True)
    aideen = models.TextField(blank=True, null=True)
    qstyle = models.CharField(blank=True, null=True, max_length=45,)
    parentvarname = models.CharField(blank=True, null=True, max_length=45,)
    section = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['questionno']

    def __str__(self):
        return '%s' % self.questionen


#######################
## listes de valeurs des questions de typequestion_id=4 (CATEGORIAL)
# Pour les questions qui aparaissent rarement et dont les réponses sont des listes de valeur
class Reponsepajsm(models.Model):
    question = models.ForeignKey(Questionpajsm, on_delete=models.DO_NOTHING)
    reponse_no = models.CharField(max_length=200)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    varname = models.CharField(blank=True, null=True, max_length=45,)

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_en


#######################
## Enregistrement des reponses des donnees NON repetitives (étude)
class Resultatpajsm(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    question = models.ForeignKey(Questionpajsm, on_delete=models.CASCADE)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reponsetexte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accompagnement = models.ForeignKey(Accompagnement, on_delete=models.DO_NOTHING, default=1)

    class Meta:
        # constraints = [models.UniqueConstraint(fields=['personne', 'assistant', 'question'], name='unique_result')]
        # unique_together = (('personne', 'assistant', 'question', 'accompagnement'),)
        # indexes = [models.Index(fields=['personne', 'assistant', 'question', 'accompagnement'])]
        # constraints = [models.UniqueConstraint(fields=['personne', 'question'], name='unique_result')]
        unique_together = (('personne', 'question', 'accompagnement'),)
        indexes = [models.Index(fields=['personne', 'question', 'accompagnement'])]

    def __str__(self):
        return '%s' % self.reponsetexte


#######################
## Enregistrement des reponses des donnees REPETITIVES (étude)
# Garder le questionnaire_id pour pouvoir effacer une fiche au complet sans faire une requete compliquée
DEFAULT_DATE = '0000-00-00'


class Resultatrepetpajsm(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    assistant = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    questionnaire = models.ForeignKey(Questionnaire, db_index=True, on_delete=models.DO_NOTHING)
    fiche = models.IntegerField(db_index=True)
    question = models.ForeignKey(Questionpajsm, db_index=True, on_delete=models.CASCADE)
    reponsetexte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accompagnement = models.ForeignKey(Accompagnement, on_delete=models.DO_NOTHING, default=1)

    class Meta:
        # constraints = [models.UniqueConstraint(fields=['personne', 'assistant', 'questionnaire', 'question', 'fiche'], name='unique_repet')]
        # unique_together = ('personne', 'assistant', 'questionnaire', 'question', 'accompagnement', 'fiche')
        # ordering = ['personne', 'assistant', 'questionnaire', 'question', 'fiche']
        # indexes = [models.Index(fields=['personne', 'assistant', 'questionnaire', 'question', 'accompagnement', 'fiche'])]
        # constraints = [models.UniqueConstraint(fields=['personne', 'assistant', 'questionnaire', 'question', 'fiche'], name='unique_repet')]
        unique_together = ('personne', 'questionnaire', 'question', 'accompagnement', 'fiche')
        ordering = ['personne', 'questionnaire', 'question', 'fiche']
        indexes = [models.Index(fields=['personne', 'questionnaire', 'question', 'accompagnement', 'fiche'])]

    def __str__(self):
        return '%s' % self.reponsetexte


############################################
# Pour l'enquete aupres des intervenants et aparentes (enquete)
class Resultatenquete(models.Model):
    intervenant = models.ForeignKey(Intervenant, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, db_index=True, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Questionpajsm, db_index=True, on_delete=models.CASCADE)
    reponsetexte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # constraints = [models.UniqueConstraint(fields=['personne', 'assistant', 'questionnaire', 'question', 'fiche'], name='unique_repet')]
        unique_together = ('intervenant', 'questionnaire', 'question')
        ordering = ['intervenant', 'questionnaire', 'question']
        indexes = [models.Index(fields=['intervenant', 'questionnaire', 'question'])]

    def __str__(self):
        return '%s' % self.reponsetexte


class Vignette(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    description_txt_en = models.TextField()
    description_txt_fr = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.reponse_valeur
