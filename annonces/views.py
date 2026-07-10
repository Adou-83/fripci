from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Annonce, Favori
from .forms import AnnonceForm


# DETAIL
def detail(request, pk):

    annonce = get_object_or_404(Annonce, pk=pk)

    est_favori = False

    if request.user.is_authenticated:
        est_favori = Favori.objects.filter(
            utilisateur=request.user,
            annonce=annonce
        ).exists()

    return render(request, "annonces/detail.html", {
        "annonce": annonce,
        "est_favori": est_favori
    })


# CREATE
@login_required
def create_annonce(request):

    if request.method == "POST":
        form = AnnonceForm(request.POST, request.FILES)

        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.vendeur = request.user
            annonce.save()
            return redirect("detail", pk=annonce.pk)

    else:
        form = AnnonceForm()

    return render(request, "annonces/create.html", {
        "form": form
    })


# UPDATE
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

        if form.is_valid():
            form.save()
            return redirect("detail", pk=annonce.pk)

    else:
        form = AnnonceForm(instance=annonce)

    return render(request, "annonces/update.html", {
        "form": form,
        "annonce": annonce
    })


# DELETE
@login_required
def delete_annonce(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk,
        vendeur=request.user
    )

    if request.method == "POST":
        annonce.delete()
        return redirect("mes_annonces")

    return render(request, "annonces/delete.html", {
        "annonce": annonce
    })


# MES ANNONCES
@login_required
def mes_annonces(request):

    annonces = Annonce.objects.filter(
        vendeur=request.user
    ).order_by("-premium", "-cree_le")

    return render(request, "annonces/mes_annonces.html", {
        "annonces": annonces
    })


# BOOST PREMIUM
@login_required
def boost_annonce(request, pk):

    annonce = get_object_or_404(
        Annonce,
        pk=pk,
        vendeur=request.user
    )

    if not annonce.premium:
        annonce.premium = True
        annonce.boost_le = timezone.now()
        annonce.save()

    return redirect("mes_annonces")


# AJOUT FAVORI
@login_required
def ajouter_favori(request, pk):

    annonce = get_object_or_404(Annonce, pk=pk)

    Favori.objects.get_or_create(
        utilisateur=request.user,
        annonce=annonce
    )

    return redirect("detail", pk=pk)


# SUPPRIMER FAVORI
@login_required
def supprimer_favori(request, pk):

    annonce = get_object_or_404(Annonce, pk=pk)

    Favori.objects.filter(
        utilisateur=request.user,
        annonce=annonce
    ).delete()

    return redirect("detail", pk=pk)


# MES FAVORIS
@login_required
def mes_favoris(request):

    favoris = Favori.objects.filter(
        utilisateur=request.user
    ).select_related("annonce")

    return render(request, "annonces/mes_favoris.html", {
        "favoris": favoris
    })
    
    
@login_required
def dashboard(request):

    annonces = Annonce.objects.filter(vendeur=request.user)

    total_annonces = annonces.count()

    annonces_premium = annonces.filter(
        premium=True
    ).count()

    total_favoris = Favori.objects.filter(
        annonce__vendeur=request.user
    ).count()

    dernieres_annonces = annonces.order_by(
        "-cree_le"
    )[:5]

    context = {
        "total_annonces": total_annonces,
        "annonces_premium": annonces_premium,
        "total_favoris": total_favoris,
        "dernieres_annonces": dernieres_annonces,
    }

    return render(
        request,
        "annonces/dashboard.html",
        context
    )