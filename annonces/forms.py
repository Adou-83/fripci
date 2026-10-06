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

        labels = {
            "titre": "Titre de l'annonce",
            "categorie": "Catégorie",
            "prix": "Prix (FCFA)",
            "ville": "Ville",
            "description": "Description",
            "image": "Photo principale",
        }

        widgets = {
            "titre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : Chemise Ralph Lauren"
                }
            ),

            "categorie": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "prix": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : 15000"
                }
            ),

            "ville": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex : Abidjan"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Décrivez l'article..."
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*"
                }
            ),
        }