from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True)
    ville = models.CharField(max_length=100, blank=True)

    ESTATUT_CHOICES = [
        ("client", "Client"),
        ("vendeur", "Vendeur"),
    ]

    statut = models.CharField(
        max_length=20,
        choices=ESTATUT_CHOICES,
        default="client"
    )

    def __str__(self):
        return self.username