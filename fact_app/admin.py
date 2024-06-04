from django.contrib import admin
from .models import *


class AdminEmployer(admin.ModelAdmin):
    list_display = ('name', 'prenom', 'telephone', 'departement', 'created_date')


class AdminDemande(admin.ModelAdmin):
    list_display = ('employer', 'demande_date', 'type_compte', 'type_achat', 'last_update', 'valider')


admin.site.register(Employer, AdminEmployer)
admin.site.register(Demande, AdminDemande)
admin.site.register(Compte)
admin.site.register(Departement)
admin.site.register(Fournisseur)
admin.site.register(Article)

