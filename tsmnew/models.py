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


class Public(models.Model):
    description = models.CharField(max_length=100, verbose_name="Type d'informations pouvant être rendues publiques")

    class Meta:
        ordering = ['description']

    def __str__(self):
        return '%s' % self.description


class Echecconditions(models.Model):
    description = models.CharField(max_length=100, verbose_name="Non respect des conditionsCauses d'échec")

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


class Pajnew(models.Model):
    nom = models.CharField(max_length=250,verbose_name="1) * Nom du programme")
    sigle = models.CharField(max_length=250,verbose_name="1) Sigle ou acronyme du programme", blank=True, null=True)
    adresse = models.TextField(verbose_name="Adresse civique du programme (point de chute)", blank=True, null=True)
    nomresponsable = models.CharField(max_length=250,verbose_name="2) * Qui est la personne responsable?", blank=True, null=True)
    formationresponsable = models.CharField(max_length=250,verbose_name="2) Quelle est sa formation?", blank=True, null=True)
    courrielresponsable = models.CharField(max_length=250,verbose_name="2) Courriel du responsable du programme", blank=True, null=True)
    telresponsable = models.CharField(max_length=250,verbose_name="2) Tel du responsable du programme", blank=True, null=True)
    titreresponsable = models.CharField(max_length=250,verbose_name="2) Titre ou occupation du responsable du programme", blank=True, null=True)
    confidentiel = models.BooleanField(verbose_name="* Cocher si ces informations sont confidentielles")
    public = models.ManyToManyField(Public, default='1', verbose_name="* Autorisation à rendre public les coordonnées de la personne responsable (sur le site Web de l’Osbervatoire ?)")
    nomrepondant = models.CharField(max_length=250,verbose_name="Nom du répondant a questionnaire", blank=True, null=True)
    courrielrepondant = models.CharField(max_length=250,verbose_name="Courriel du répondant a questionnaire", blank=True, null=True)
    telrepondant = models.CharField(max_length=250,verbose_name="Tel du répondant a questionnaire", blank=True, null=True)
    siteweb = models.CharField(max_length=250,verbose_name="3) * Adresse du site web du programme", blank=True, null=True)
    rapportannuel = models.BooleanField(verbose_name="4) * Cocher s'il y a un rapport annuel")
    rapportannuelpublic = models.BooleanField(verbose_name="4) * Cocher si le rapport annuel peut être rendu public")
    tsmfile = models.FileField(upload_to='DocsReferences', verbose_name="4a) Rapport annuel de ce programme ou de la documentation utile", help_text="ATTENTION PAS D'ACCENT DANS LE NOM DU FICHIER", blank=True, null=True)
    debut = models.CharField(max_length=250,verbose_name="5) * Depuis quand ce programme existe-t-il? (mois et année si possible)", blank=True, null=True)
    objectifs = models.TextField(verbose_name="6) * Objectifs du programme (résumé)", blank=True, null=True)
    clientele = models.TextField(verbose_name="7) Clientèle cible du programme", blank=True, null=True)
    territoire = models.CharField(max_length=250,verbose_name="9) Quelle juridiction territoriale votre programme dessert-il?", blank=True, null=True)
    affiliation = models.CharField(max_length=250,verbose_name="11) À quel(s) tribunal/aux votre programme est-il affilié?", blank=True, null=True)
    municipalites = models.CharField(max_length=250,verbose_name="10) Municipalités desservies par votre programmme", blank=True, null=True)
    etapejudiciaire = models.ManyToManyField(Judiciaires, default='1',verbose_name="8) * À quelle étape du processus judiciaire les participants sont-ils référés au programme?")
    etapejudiciairtxt = models.TextField(verbose_name="8 +)Détails", blank=True, null=True)
    reference = models.ManyToManyField(References, default='1', verbose_name="9) * De qui proviennent les références de vos participants à ce programme?")
    referencetxt = models.TextField(verbose_name="9+) Détails", blank=True, null=True)
    prerequis = models.ManyToManyField(Prerequis, default='1', verbose_name="10) * Quels sont les critères d’admissibilité?")
    age = models.ForeignKey(Ages, verbose_name="10+) Quels sont les critères d'age?", blank=True, null=True, on_delete=models.DO_NOTHING)
    typedelits = models.ManyToManyField(Delits, default='1', verbose_name="10+) Types de délits ou d'accusations acceptés")
    prerequistexte = models.TextField(verbose_name="10 suite) Précisions sur les critères d’admissibilité", blank=True, null=True)
    exclusions = models.ManyToManyField(Exclus, default='1', verbose_name="11) * Quels sont les critères d’exclusion?")
    exclusiontexte = models.TextField(verbose_name="11 suite) Détails", blank=True, null=True)
    decision = models.ManyToManyField(Decisions, default='1', verbose_name="12) Qui a un pouvoir décisionnel sur l’admission au programme")
    decisionpouvoir = models.TextField(verbose_name="12+) Comment la décision est-elle prise?", blank=True, null=True)
    delais = models.CharField(max_length=250,verbose_name="13) Quels sont les délais d’attente après avoir inscrit une demande?", blank=True, null=True)
    traitementtype = models.ManyToManyField(Typetraitements, default='1', verbose_name="14) * Quels sont les services offerts aux participants?")
    traitementtexte = models.TextField(verbose_name="14a) Détails sur les services offerts aux participants", blank=True, null=True)
    condition = models.ManyToManyField(Conditions, default='1', verbose_name="15) * Quelles sont les conditions à respecter une fois dans le programme?")
    conditiontexte = models.TextField(verbose_name="15a) Détails des conditions", blank=True, null=True)
    respectcondition = models.BooleanField(verbose_name="16) Est-ce que le respect des conditions indiquées à la question 15 mène à la réussite du programme?(Cocher si OUI)")
    reussitedef = models.TextField(verbose_name="16b) Si non, qu’est-ce qui entraîne la réussite du programme?", blank=True, null=True)
    echeccondition = models.ManyToManyField(Echecconditions, default='1', verbose_name="17) * Quelles conséquences s’appliquent en cas de non-respect des conditions?")
    echecconditiontexte = models.TextField(verbose_name="17a) Non respects détails", blank=True, null=True)
    echecmotif = models.ManyToManyField(Echecmotifs, default='1', verbose_name="S6- Quels sont les motifs les plus fréquents d'échec du programme?")
    echectexte = models.TextField(verbose_name="17--a) Précisions sur les motifs d’échec", blank=True, null=True)
    succes = models.ManyToManyField(Succes, default='1', verbose_name="18) * Qu’arrive-t-il lorsque le programme est complété avec succès?")
    succestexte = models.TextField(verbose_name="18a) Succès détails", blank=True, null=True)
    finbool = models.BooleanField(verbose_name="19) À la fin du programme, faites-vous une transition vers un suivi en communauté?(Cocher si OUI)")
    fintexte = models.TextField(verbose_name="19a) Si oui : comment assurez-vous la transition vers ce suivi?", blank=True, null=True)
    progdureebool = models.BooleanField(verbose_name="20) La participation au programme est-elle d’une durée prédéterminée?(Cocher si OUI)")
    traitementduree = models.CharField(max_length=250,verbose_name="20a) Si oui: quelle est-elle?", blank=True, null=True)
    traitementmin = models.CharField(max_length=250,verbose_name="20b) Durée maximale", blank=True, null=True)
    traitementmax = models.CharField(max_length=250,verbose_name="20b) Durée minimale", blank=True, null=True)
    autreprogramme = models.BooleanField(verbose_name="21) Y a-t-il d’autres programmes proposant des alternatives à l’incarcération ou à la judiciarisation dans votre juridiction?(Cocher si OUI)")
    autreprogramtexte = models.TextField(verbose_name="21a) Si oui : lesquels?", blank=True, null=True)
    autreaffilie = models.BooleanField(verbose_name="21b) Sont-ils affiliés à votre programme?(Cocher si OUI)")
    partenariat = models.ManyToManyField(Partenaires, default='1', verbose_name="22) Avez-vous établi des partenariats avec d’autres services ou organisations?")
    partenariattexte = models.TextField(verbose_name="22a) Si oui :  précisions sur les partenariats", blank=True, null=True)
    caseload = models.CharField(max_length=250,verbose_name="P3- Nombre de dossier à charge de l’intervenant-pivot ou agent de liaison", blank=True, null=True)
    limiteparticipants = models.BooleanField(verbose_name="S1- Avez-vous une limite de participants?(Cocher si OUI)")
    limitenb = models.TextField(verbose_name="S1a- Si oui, à combien est établie la limite actuelle ?", blank=True, null=True)
    partactif = models.CharField(max_length=250, verbose_name="S2- Combien avez-vous de participants actifs actuellement?", blank=True, null=True)
    autrejur = models.BooleanField(verbose_name="S3- Recevez-vous des participants d’autres juridictions?(Cocher si OUI)")
    autrejurtext = models.TextField(verbose_name="S3a- Si oui: dans quelles circonstances?", blank=True, null=True)
    partmoyen = models.CharField(max_length=250, verbose_name="S4- En moyenne, combien de nouveaux participants intègrent le programme chaque mois?", blank=True, null=True)
    nbreussi = models.CharField(max_length=250, verbose_name="S5a- Combien de participants ont complété le programme dans la dernière année?", blank=True, null=True)
    nbreussitxt = models.CharField(max_length=250, verbose_name="S5a-a- Détails sur Combien de participants ont complété le programme dans la dernière année?", blank=True, null=True)
    nbechoue = models.CharField(max_length=250,  verbose_name="S5b- Combien de participants ont échoué au programme dans la dernière année?", blank=True, null=True)
    nbsuccesdebut = models.CharField(max_length=250,  verbose_name="S5c- Nombre de participants ayant achevé le programme avec succès depuis son entrée en opération?", blank=True, null=True)
    nbechouedebut = models.CharField(max_length=250,  verbose_name="S5d- Nombre de participants ayant échoué depuis l’entrée en opération du programme (incluant les retraits volontaires)", blank=True, null=True)
    evaluation = models.BooleanField(verbose_name="4) * Votre programme a-t-il déjà fait l’objet d’une évaluation?(Cocher si OUI)")
    evalquand= models.CharField(max_length=250,verbose_name="4a) Quand est-ce que cette évaluation a eu lieu?", blank=True, null=True)
    evaltype = models.ForeignKey(Evaluations, verbose_name="4b) Quel type était-ce? ", blank=True, null=True, on_delete=models.DO_NOTHING)
    evalqui= models.CharField(max_length=250,verbose_name="4c) Par qui cette évaluation a-t-elle été réalisée?", blank=True, null=True)
    resume = models.TextField(verbose_name="4d) Quels sont les résultats de cette évaluation?", blank=True, null=True)
    evaluationfuture = models.BooleanField(verbose_name=" * (si non évalué) Une évaluation du programme est-elle prévue?(Cocher si OUI)")
    evafuturedetail = models.TextField(verbose_name="(si prévue) Quand, quel type et par qui le programme sera évalué?", blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    reunionfreq = models.TextField(verbose_name="Fréquence des réunions de l’équipe", blank=True, null=True)
    audiencefreq = models.CharField(max_length=250,verbose_name="Fréquence des audiences", blank=True, null=True)
    #surveillance = models.ManyToManyField(Surveillances, default='1', verbose_name="Surveillance du programme")
    cadreref = models.FileField(upload_to='DocsReferences', verbose_name="Cadre de référence ou document constitutif (qui encadre le fonctionnement du PAJ)", help_text="ATTENTION PAS D'ACCENT DANS LE NOM DU FICHIER", blank=True, null=True)
    cadrerefpublic = models.BooleanField(verbose_name="Cocher si le le cadre de référence peut être rendu public")
    equipenb = models.CharField(max_length=250,verbose_name="nombre de membres de l'équipe courante", blank=True, null=True)

    def __str__(self):
        return '%s' % self.nom


class Equipe(models.Model):
    tribunal = models.ForeignKey(Pajnew, on_delete=models.DO_NOTHING)
    profession = models.ForeignKey(Professionnels, on_delete=models.DO_NOTHING,verbose_name="* Professionnels" )
    nombre = models.IntegerField(default=0)
    duree = models.CharField(max_length=250, verbose_name="Temps de travail",blank=True, null=True)
    tache = models.TextField(blank=True, null=True)

    class Meta:
       ordering = ['tribunal','nombre']


    def __str__(self):
        return '%s %s %s %s' % (self.profession, self.nombre, self.duree, self.tache)


class Document(models.Model):
    titrecourt = models.CharField(max_length=200, verbose_name="Non court et évocateur du document")
    documentation = models.FileField(upload_to='DocsReferences', verbose_name="ATTENTION PAS D'ACCENT DANS LE NOM DES FICHIERS", help_text="ATTENTION PAS D'ACCENT DANS LE NOM DES FICHIERS")
    tribunal = models.ForeignKey(Pajnew, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.titrecourt


class Historique(models.Model):
    modifhistoire = models.TextField(verbose_name="Description des modifications importantes")
    tribunal = models.ForeignKey(Pajnew, on_delete=models.CASCADE)
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)

