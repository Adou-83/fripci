from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_annonce, name="create_annonce"),
    path("mes-annonces/", views.mes_annonces, name="mes_annonces"),

    path("<int:pk>/edit/", views.update_annonce, name="update_annonce"),
    path("<int:pk>/delete/", views.delete_annonce, name="delete_annonce"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/boost/", views.boost_annonce, name="boost_annonce"),

    path("<int:pk>/favori/", views.ajouter_favori, name="ajouter_favori"),
    path("<int:pk>/unfavori/", views.supprimer_favori, name="supprimer_favori"),

    # ⭐ AJOUT IMPORTANT
    path("mes-favoris/", views.mes_favoris, name="mes_favoris"),
]