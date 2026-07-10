from django.contrib import admin
from .models import Categorie, Annonce, ImageAnnonce, Favori


class ImageAnnonceInline(admin.TabularInline):
    model = ImageAnnonce
    extra = 1


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):

    list_display = (
        "titre",
        "categorie",
        "prix",
        "ville",
        "vendeur",
        "premium",
        "disponible",
        "cree_le",
    )

    list_filter = (
        "categorie",
        "ville",
        "premium",
        "disponible",
    )

    search_fields = (
        "titre",
        "description",
        "marque",
    )

    readonly_fields = (
        "cree_le",
        "modifie_le",
        "boost_le",
    )

    inlines = [ImageAnnonceInline]

    list_per_page = 20


@admin.register(ImageAnnonce)
class ImageAnnonceAdmin(admin.ModelAdmin):

    list_display = (
        "annonce",
        "id",
    )

    search_fields = (
        "annonce__titre",
    )
    
@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):

    list_display = (
        "utilisateur",
        "annonce",
        "cree_le",
    )