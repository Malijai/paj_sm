# pour les DICHO (8)= Yes_No
CHOIX_ON = {
    1: 'Oui',
    0: 'Non'
    }

# pour les autres (dichou 24= Yes_No_Unknown)
CHOIX_ONUK = {
    1: 'Oui',
    0: 'Non',
    99: 'Non-spécifié'
    }

# 18 pour les ONNSP (18 = Oui-Non-Ne sait pas)
CHOIX_ONNSP = {
    1: 'Oui',
    0: 'Non',
    997: 'Ne sais pas'
    }

# pour les ONNSP (11 = Vrai-Faux-Ne sait pas)
CHOIX_VFNSP = {
    1: 'Vrai',
    0: 'Faux',
    997: 'NSP'
    }

# 15
CHOIX_MOINSPLUS = {
    1: '-5 Atténuante',
    2: '-4',
    3: '-3',
    4: '-2',
    5: '-1',
    6: '0 Neutre',
    7: '1',
    8: '2',
    9: '3',
    10: '4',
    11: '5 Aggravante',
    }

# 13
CHOIX_UNDIX = {
    1: '1 Pas du tout',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10 Tout a fait',
    }

# 9
CHOIX_UNCINQ = {
    1: '1 Pas du tout',
    2: '2',
    3: '3 Neutre',
    4: '4',
    5: '5 Absolument',
    }

# 10
CHOIX_UNSIX = {
    1: '1 Fortement en désaccord',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: "6 Fortement d'accord",
    }

# 16
CHOIX_UNCINQ2 = {
    1: 'Fortement en accord',
    2: 'En accord',
    3: 'Ni en accord ni en désaccord',
    4: 'En désaccord',
    5: 'Fortement en désaccord',
    }

# pour les DICHO (8)= Yes_No
CHOIX_ETUDIANT = {
    1: 'Avocat',
    0: 'Ni Avocat ni étudiant',
    2: 'Étudiant',
    }

TEXTES_MESSAGES = {
    'Refus1': "Merci. Votre refus de participer est enregistré, vous ne serez plus solicité pour cette enquête !",
    'Consent': "Merci pour votre consentement à participer",
    'Rejet1': "Ce questionnaire n'est plus disponible pour la personne ayant cette adresse de courriel.",
    'Erreur': "Il y a une erreur, contactez malijai.caulet.ippm@ssss.gouv.qc.ca>",
    'Complet1': "Vous avez déjà répondu à toutes les questions de cette enquête. Merci !",
    'Refus2': "Vous avez déjà refusé de participer à cette enquête, si vous avez changé d'avis contactez la coordonnatrice du projet dont les coordonnées sont en bas de page!",
    'Incompatible': "Certaines de vos réponses sont incompatibles, s'il vous plait recommencez !",
    'Termine': "Questionnaire terminé, Merci pour votre participation !",
    'Termine2': "Vous avez déjà répondu a toutes les questions de cette enquête, Merci pour votre participation !",
    'AR': "Merci d'avoir soumis votre adresse, un message avec le lien pour participer vous a été envoyé à l'adresse suivante : ",
    'Vides': "Il y a trop de questions sans réponse, veuillez vérifier cette section s'il vous plait"
}