from django import forms
from pajsm.etude.models import Intervenant


class IntervenantForm(forms.ModelForm):
    class Meta:
        model = Intervenant
        fields = ['courriel',]
        exclude = ()
