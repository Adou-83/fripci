from django.shortcuts import render
from annonces.models import Annonce, Categorie


def home(request):

    annonces = Annonce.objects.select_related(
        'categorie',
        'vendeur'
    ).filter(
        disponible=True
    )

    recherche = request.GET.get('q')

    if recherche:
        annonces = annonces.filter(
            titre__icontains=recherche
        )

    categorie_id = request.GET.get('categorie')

    if categorie_id:
        annonces = annonces.filter(
            categorie_id=categorie_id
        )

    ville = request.GET.get('ville')

    if ville:
        annonces = annonces.filter(
            ville__icontains=ville
        )

    # Premium en premier puis les plus récentes
    annonces = annonces.order_by(
        '-premium',
        '-cree_le'
    )

    categories = Categorie.objects.all()

    villes = Annonce.objects.values_list(
        'ville',
        flat=True
    ).distinct()

    return render(
        request,
        'core/home.html',
        {
            'annonces': annonces,
            'categories': categories,
            'villes': villes,
        }
    )