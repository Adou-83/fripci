from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Annonce, ImageAnnonce, Favori
from .forms import AnnonceForm


# ==========================================================
# DASHBOARD
# ==========================================================

@login_required
def dashboard(request):

    annonces = Annonce.objects.filter(
        vendeur=request.user
    ).order_by("-cree_le")

    favoris = Favori.objects.filter(
        utilisateur=request.user
    ).select_related("annonce")

    return render(
        request,
        "annonces/dashboard.html",
        {
            "annonces": annonces,
            "favoris": favoris,
        }
    )


# ==========================================================
# DETAIL D'UNE ANNONCE
# ==========================================================

def detail(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk
    )

    return render(
        request,
        "annonces/detail.html",
        {
            "annonce": annonce
        }
    )


# ==========================================================
# CREER UNE ANNONCE
# ==========================================================

@login_required
def create_annonce(request):

    if request.method == "POST":

        form = AnnonceForm(
            request.POST,
            request.FILES
        )

        # Photos supplémentaires
        images = request.FILES.getlist("images")

        # Maximum 4 photos supplémentaires
        if len(images) > 4:

            form.add_error(
                None,
                "Vous pouvez ajouter au maximum 4 photos supplémentaires."
            )

        if form.is_valid():

            annonce = form.save(
                commit=False
            )

            annonce.vendeur = request.user

            annonce.save()

            # Enregistrer les photos supplémentaires
            for image in images:

                ImageAnnonce.objects.create(
                    annonce=annonce,
                    image=image
                )

            return redirect(
                "detail",
                pk=annonce.pk
            )

    else:

        form = AnnonceForm()

    return render(
        request,
        "annonces/create.html",
        {
            "form": form
        }
    )


# ==========================================================
# MODIFIER UNE ANNONCE
# ==========================================================

@login_required
def update_annonce(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk,
        vendeur=request.user
    )

    if request.method == "POST":

        form = AnnonceForm(
            request.POST,
            request.FILES,
            instance=annonce
        )

        # Nouvelles photos
        images = request.FILES.getlist("images")

        # Nombre de photos supplémentaires déjà présentes
        images_existantes = annonce.images.count()

        # Maximum 4 photos supplémentaires
        if images_existantes + len(images) > 4:

            form.add_error(
                None,
                "Une annonce peut contenir au maximum 4 photos supplémentaires."
            )

        if form.is_valid():

            form.save()

            for image in images:

                ImageAnnonce.objects.create(
                    annonce=annonce,
                    image=image
                )

            return redirect(
                "detail",
                pk=annonce.pk
            )

    else:

        form = AnnonceForm(
            instance=annonce
        )

    return render(
        request,
        "annonces/update.html",
        {
            "form": form,
            "annonce": annonce
        }
    )


# ==========================================================
# SUPPRIMER UNE ANNONCE
# ==========================================================

@login_required
def delete_annonce(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk,
        vendeur=request.user
    )

    if request.method == "POST":

        annonce.delete()

        return redirect(
            "mes_annonces"
        )

    return render(
        request,
        "annonces/delete.html",
        {
            "annonce": annonce
        }
    )


# ==========================================================
# MES ANNONCES
# ==========================================================

@login_required
def mes_annonces(request):

    annonces = Annonce.objects.filter(
        vendeur=request.user
    ).order_by("-id")

    return render(
        request,
        "annonces/mes_annonces.html",
        {
            "annonces": annonces
        }
    )


# ==========================================================
# BOOST PREMIUM
# ==========================================================

@login_required
def boost_annonce(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk,
        vendeur=request.user
    )

    annonce.premium = True

    annonce.boost_le = timezone.now()

    annonce.save()

    return redirect(
        "mes_annonces"
    )


# ==========================================================
# AJOUTER AUX FAVORIS
# ==========================================================

@login_required
def ajouter_favori(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk
    )

    Favori.objects.get_or_create(
        utilisateur=request.user,
        annonce=annonce
    )

    return redirect(
        "detail",
        pk=pk
    )


# ==========================================================
# RETIRER DES FAVORIS
# ==========================================================

@login_required
def supprimer_favori(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk
    )

    Favori.objects.filter(
        utilisateur=request.user,
        annonce=annonce
    ).delete()

    return redirect(
        "detail",
        pk=pk
    )


# ==========================================================
# MES FAVORIS
# ==========================================================

@login_required
def mes_favoris(request):

    favoris = Favori.objects.filter(
        utilisateur=request.user
    ).select_related(
        "annonce"
    )

    return render(
        request,
        "annonces/mes_favoris.html",
        {
            "favoris": favoris
        }
    )