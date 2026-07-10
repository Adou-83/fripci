from django import forms
from .models import Annonce


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = [
            "titre",
            "categorie",
            "prix",
            "ville",
            "description",
            "image",
        ]