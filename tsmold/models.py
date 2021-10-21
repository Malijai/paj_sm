# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Delits(models.Model):
    #violent; sexuel ...
    description = models.CharField(max_length=100, verbose_name="Types de délits")

    class Meta:
       ordering = ['description']

    def __str__(self):
       return '%s' % self.description


class Ages(models.Model):
    #mineurs + majeurs; majeurs seulement ...
    description = models.CharField(max_length=100, verbose_name="Classes d'ages")

    class Meta:
       ordering = ['description']

    def __str__(self):
       return '%s' % self.description


class Diagnostics(models.Model):
    description = models.CharField(max_length=100, verbose_name="Types de diagnostics")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Decisions(models.Model):
    description = models.CharField(max_length=100, verbose_name="Auteurs des décisions")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Prerequis(models.Model):
    description = models.CharField(max_length=100, verbose_name="Prérequis")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Typetraitements(models.Model):
    description = models.CharField(max_length=100, verbose_name="Types de traitements")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Echecs(models.Model):
    description = models.CharField(max_length=100, verbose_name="Conséquences en cas de non suivi du programme")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Succes(models.Model):
    description = models.CharField(max_length=100, verbose_name="Conséquences en cas d'adhérence au programme")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Surveillances(models.Model):
    description = models.CharField(max_length=100, verbose_name="Surveillance")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Fins(models.Model):
    description = models.CharField(max_length=100, verbose_name="Achèvement du programme")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Judiciaires(models.Model):
    # étapes judiciaires
    description = models.CharField(max_length=100, verbose_name="Étapes judiciaires")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class References(models.Model):
    description = models.CharField(max_length=100, verbose_name="Références au programme")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Exclus(models.Model):
    description = models.CharField(max_length=100, verbose_name="Exclusions du programme")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Conditions(models.Model):
    description = models.CharField(max_length=100, verbose_name="Conditions")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Partenaires(models.Model):
    description = models.CharField(max_length=100, verbose_name="Partenaire")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Professionnels(models.Model):
    description = models.CharField(max_length=100, verbose_name=" * Professionnels")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Reunions(models.Model):
    description = models.CharField(max_length=100, verbose_name="Réunions")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Limites(models.Model):
    description = models.CharField(max_length=100, verbose_name="Limites")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Echecmotifs(models.Model):
    description = models.CharField(max_length=100, verbose_name="Causes d'échec")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Evaluations(models.Model):
    description = models.CharField(max_length=100, verbose_name="Évaluations")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Pajold(models.Model):
    nom = models.CharField(max_length=250,verbose_name="1) * Nom du programme")
    province = models.CharField(max_length=250,verbose_name="1a) Province où se situe ce programme", blank=True, null=True)
    adresse = models.TextField(verbose_name="Adresse complète du programme", blank=True, null=True)
    nomresponsable = models.CharField(max_length=250,verbose_name="2) * Qui est la personne responsable?", blank=True, null=True)
    formationresponsable = models.CharField(max_length=250,verbose_name="2) Quelle est sa formation?", blank=True, null=True)
    responcontact = models.BooleanField(verbose_name="2a) Cliquer si c'est la personne à contacter si nous nemons une étude ultérieure")
    siteweb = models.CharField(max_length=250,verbose_name="3) * Adresse du site web du programme", blank=True, null=True)
    rapportannuel = models.BooleanField(verbose_name="4) * Cliquer s'il y a un rapport annuel")
    tsmfile = models.FileField(upload_to='DocsReferences', verbose_name="4a) Rapport annuel de ce programme ou de la documentation utile", help_text="ATTENTION PAS D'ACCENT DANS LE NOM DU FICHIER", blank=True, null=True)
    debut = models.CharField(max_length=250,verbose_name="5) * Depuis quand ce programme existe-t-il? (mois et année si possible)", blank=True, null=True)
    objectifs = models.TextField(verbose_name="6) * Objectifs du programme", blank=True, null=True)
    clientele = models.TextField(verbose_name="7) Clientèle cible du programme", blank=True, null=True)
    etapejudiciaire = models.ManyToManyField(Judiciaires, default='1',verbose_name="8) * À quelle étape du processus judiciaire les participants sont-ils référés au programme?")
    etapejudiciairtxt = models.TextField(verbose_name="8 +)Détails", blank=True, null=True)
    reference = models.ManyToManyField(References, default='1', verbose_name="9) * De qui proviennent les références de vos participants à ce programme?")
    referencetxt = models.TextField(verbose_name="9+) Détails", blank=True, null=True)
    prerequis = models.ManyToManyField(Prerequis, default='1', verbose_name="10) * Quels sont les critères d’admissibilité?")
    age = models.ManyToManyField(Ages, verbose_name="10+) Quels sont les critères d'age?")
    diagnostic = models.ManyToManyField(Diagnostics, default='1', verbose_name="10+) Diagnostics ou antécédents psychiatriques admis")
    typedelits = models.ManyToManyField(Delits, default='1', verbose_name="10+) Types de délits ou d'accusations acceptés")
    prerequistexte = models.TextField(verbose_name="10 suite) Détails", blank=True, null=True)
    exclusions = models.ManyToManyField(Exclus, default='1', verbose_name="11) * Quels sont les critères d’exclusion?")
    exclusiontexte = models.TextField(verbose_name="11 suite) Détails", blank=True, null=True)
    decision = models.ManyToManyField(Decisions, default='1', verbose_name="12) Qui a un pouvoir décisionnel sur l’admission au programme")
    decisionpouvoir = models.TextField(verbose_name="12+) Comment la décision est-elle prise?", blank=True, null=True)
    delais = models.CharField(max_length=250,verbose_name="13) Quels sont les délais d’attente après avoir inscrit une demande?", blank=True, null=True)
    traitementtype = models.ManyToManyField(Typetraitements, default='1', verbose_name="14) * Quels sont les services offerts aux participants?")
    traitementtexte = models.TextField(verbose_name="14a) Détails sur les services offerts aux participants", blank=True, null=True)
    medication = models.BooleanField(verbose_name="Cliquer si une médication est obligatoire")
    condition = models.ManyToManyField(Conditions, default='1', verbose_name="15) * Quelles sont les conditions à respecter une fois dans le programme?")
    conditiontexte = models.TextField(verbose_name="15a) Détails des conditions", blank=True, null=True)
    respectcondition = models.BooleanField(verbose_name="16) Est-ce que le respect des conditions indiquées à la question 15 mène à la réussite du programme?")
    reussitedef = models.TextField(verbose_name="16b) Si non, qu’est-ce qui entraîne la réussite du programme?", blank=True, null=True)
    echec = models.ManyToManyField(Echecs, default='1', verbose_name="17) * Quelles conséquences s’appliquent en cas de non-respect des conditions?")
    echectexte = models.TextField(verbose_name="17a) Non respects détails", blank=True, null=True)
    succes = models.ManyToManyField(Succes, default='1', verbose_name="18) * Qu’arrive-t-il lorsque le programme est complété avec succès?")
    succestexte = models.TextField(verbose_name="18a) Succès détails", blank=True, null=True)
    finbool = models.BooleanField(verbose_name="19) À la fin du programme, faites-vous une transition vers un suivi en communauté?")
    fintexte = models.TextField(verbose_name="19a) Si oui : comment assurez-vous la transition vers ce suivi?", blank=True, null=True)
    progdureebool = models.BooleanField(verbose_name="20) La participation au programme est-elle d’une durée prédéterminée?")
    traitementduree = models.CharField(max_length=250,verbose_name="20a) Si oui: quelle est-elle?", blank=True, null=True)
    traitementmin = models.CharField(max_length=250,verbose_name="20b) Durée maximale", blank=True, null=True)
    traitementmax = models.CharField(max_length=250,verbose_name="20b) Durée minimale", blank=True, null=True)
    surveillance = models.ManyToManyField(Surveillances, default='1', verbose_name="Surveillance du programme")
    issue = models.ManyToManyField(Fins, default='1', verbose_name="Achèvement du programme par :")
    autreprogramme = models.BooleanField(verbose_name="21) Y a-t-il d’autres programmes proposant des alternatives à l’incarcération ou à la judiciarisation dans votre juridiction?")
    autreprogramtexte = models.TextField(verbose_name="21a) Si oui : lesquels?", blank=True, null=True)
    autreaffilie = models.BooleanField(verbose_name="21b) Sont-ils affiliés à votre programme?")
    partenariat = models.ManyToManyField(Partenaires, default='1', verbose_name="22) Avez-vous établi des partenariats avec d’autres services ou organisations?")
    partenariattexte = models.TextField(verbose_name="22a) Si oui : lesquels?", blank=True, null=True)
    reunionfreq = models.TextField(verbose_name="P2- Y a-t-il des réunions/discussions d’équipe? Si oui, à quelle fréquence? Qui est présent?", blank=True, null=True)
    reunionpresence = models.CharField(max_length=250,verbose_name="P3- De façon générale combien de dosiiers un intervenant peut-il avoir à sa charge?", blank=True, null=True)
    limiteparticipants = models.ForeignKey(Limites, default='1', verbose_name="S1- Avez-vous une limite de participants?", on_delete=models.DO_NOTHING)
    partactif = models.CharField(max_length=250, default=0, verbose_name="S2- Combien avez-vous de participants actifs actuellement?", blank=True, null=True)
    autrejur = models.BooleanField(verbose_name="S3- Recevez-vous des participants d’autres juridictions?")
    autrejurtext = models.TextField(verbose_name="S3a- Si oui: dans quelles circonstances?", blank=True, null=True)
    partmoyen = models.IntegerField(default=0, verbose_name="S4- En moyenne, combien de nouveaux participants intègrent le programme chaque mois?", blank=True, null=True)
    nbreussi = models.IntegerField(default=0, verbose_name="S5a- Combien de participants ont complété le programme dans la dernière année?", blank=True, null=True)
    nbreussitxt = models.TextField(verbose_name="S5a + Détails (complété le programme)", blank=True, null=True)
    nbechoue = models.IntegerField(default=0, verbose_name="S5b- Combien de participants ont échoué au programme dans la dernière année?", blank=True, null=True)
    nbechouetxt = models.TextField(verbose_name="S5b + Détails (échoué au programme)", blank=True, null=True)
    echecmotif = models.ManyToManyField(Echecmotifs, verbose_name="S6- Quels sont les motifs les plus fréquents d'échec du programme?")
    territoire = models.CharField(max_length=250,verbose_name="1) * Quelle juridiction territoriale votre programme dessert-il?", blank=True, null=True)
    affiliation = models.CharField(max_length=250,verbose_name="2) * À quel(s) tribunal/aux votre programme est-il affilié?", blank=True, null=True)
    communication = models.TextField(verbose_name="3) Avec quels autres programmes de tribunaux spécialisés en santé mentale (province ou pays) êtes vous en communication et à quelle fréquence?", blank=True, null=True)
    evaluation = models.BooleanField(verbose_name="4) * Votre programme a-t-il déjà fait l’objet d’une évaluation?")
    evalquand= models.CharField(max_length=250,verbose_name="4a) Quand est-ce que cette évaluation a eu lieu?", blank=True, null=True)
    evaltype = models.ForeignKey(Evaluations, verbose_name="4b) Quel type était-ce? ", blank=True, null=True, on_delete=models.DO_NOTHING)
    evalqui= models.CharField(max_length=250,verbose_name="4c) Par qui cette évaluation a-t-elle été réalisée?", blank=True, null=True)
    resume = models.TextField(verbose_name="4d) Quels sont les résultats de cette évaluation?", blank=True, null=True)
    evaluationfuture = models.BooleanField(verbose_name=" * (si non évalué) Une évaluation du programme est-elle prévue?")
    evafuturedetail = models.TextField(verbose_name="(si prévue) Quand, quel type et par qui le programme sera évalué?", blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    posted = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return '%s' % self.nom


class Equipe(models.Model):
    tribunal = models.ForeignKey(Pajold, on_delete=models.DO_NOTHING)
    profession = models.ForeignKey(Professionnels, on_delete=models.DO_NOTHING,verbose_name="* Professionnels" )
    nombre = models.IntegerField(default=0)
    duree = models.CharField(max_length=250, verbose_name="Temps de travail",blank=True, null=True)
    tache = models.TextField(blank=True, null=True)

    class Meta:
       ordering = ['tribunal','nombre']

    def __str__(self):
        return '%s %s %s %s' % (self.profession, self.nombre, self.duree, self.tache)
