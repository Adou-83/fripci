from django.conf import settings
from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Annonce(models.Model):

    ETAT_CHOICES = [
        ("premier_choix", "Premier choix"),
        ("tres_bon", "Très bon état"),
        ("bon", "Bon état"),
    ]

    vendeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="annonces"
    )

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE,
        related_name="annonces"
    )

    titre = models.CharField(max_length=200)
    description = models.TextField()

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    taille = models.CharField(
        max_length=20,
        blank=True
    )

    marque = models.CharField(
        max_length=100,
        blank=True
    )

    etat = models.CharField(
        max_length=20,
        choices=ETAT_CHOICES,
        default="premier_choix"
    )

    ville = models.CharField(
        max_length=100
    )

    # Image principale
    image = models.ImageField(
        upload_to="annonces/covers/"
    )

    disponible = models.BooleanField(
        default=True
    )

    # PREMIUM
    premium = models.BooleanField(
        default=False
    )

    boost_le = models.DateTimeField(
        null=True,
        blank=True
    )

    cree_le = models.DateTimeField(
        auto_now_add=True
    )

    modifie_le = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-premium", "-cree_le"]

    def __str__(self):
        return self.titre


class ImageAnnonce(models.Model):

    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="annonces/gallery/"
    )

    def __str__(self):
        return f"Image de {self.annonce.titre}"
    
    
class Favori(models.Model):
    
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE
    )

    cree_le = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "utilisateur",
            "annonce"
        )

    def __str__(self):
        return f"{self.utilisateur} - {self.annonce}"
    