from cmath import e
from urllib import request
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from .models import  Article, Compte, Departement, Employer, Demande, Fournisseur
import plotly.graph_objs as go
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from .utils import pagination, get_demande
import pdfkit
from django.template.loader import get_template, render_to_string
import datetime
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
import sys 
from compte.models import User
from django.db import transaction

def superuser_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='login/'  # Remplacez "/superuser/login/" par l'URL que vous avez définie
    )
    if function:
        return actual_decorator(function)
    return actual_decorator



class HomeView(View):
    template_name = 'index.html'

    @method_decorator(superuser_required)
    def get(self, request, *args, **kwargs):
        demandes = Demande.objects.select_related('employer').all()

        context = {'demandes': demandes}

        # PAGINATION page defaut
        default_page = 1
        page = request.GET.get('page', default_page)

        # pagination des demandes
        items_per_page = 5
        paginator = Paginator(demandes, items_per_page)
        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)

        context['demandes'] = items_page

        return render(request, self.template_name, context)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.POST.get('id_modified'):
            valider = request.POST.get('modified')
            try:
                obj = Demande.objects.get(id=request.POST.get('id_modified'))
                if valider == 'true':
                    obj.valider = True
                else:
                    obj.valider = False

                obj.save()

                messages.success(request, "Modification accomplie")
            except Exception as e:
                messages.error(request, f"Il y a une erreur {e}")

        if request.POST.get('id_supprimer'):
            try:
                demande_id = request.POST.get('id_supprimer')
                with transaction.atomic():
                    obj = Demande.objects.select_for_update().get(pk=demande_id)
                    articles = Article.objects.filter(demande=obj)
                    articles.delete()
                    obj.delete()
                    messages.success(request, "Suppression succès")
            except Exception as e:
                messages.error(request, "Erreur lors de la suppression")
        return redirect('home')


    

class AddEmployerView(View):
    template_name = 'add.employer.html'
    @method_decorator(superuser_required)
    def get(self, request, *args, **kwargs):
        departements =Departement.objects.all()
        context = {'departements': departements}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.POST.get('name'),
            'prenom': request.POST.get('prenom'),
            'telephone': request.POST.get('telephone'),
            'departement_id': request.POST.get('departement'),
        }
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            if password == "":
                User.objects.create(username=request.POST.get('name'), first_name=request.POST.get('name'), last_name=request.POST.get("prenom"), password=make_password(request.POST.get('name')), email=email)
            else:
                                User.objects.create(username=request.POST.get('name'), first_name =request.POST.get('name'), last_name=request.POST.get("prenom"), password=make_password(password), email=email)

            created = Employer.objects.create(**data)
            
            if created:
                messages.success(request, "Employer enregistré avec succès")
            else:
                messages.error(request, "Erreur lors de l'enregistrement de l'employeur")
        except Exception as e:
            messages.error(request, f"Problème lors de l'enregistrement de l'employeur : {e}")
        return redirect('add-employer')  # Redirection vers la page d'ajout d'employé

class EmployerListView(View):
    template_name = 'list_employer.html'
    @method_decorator(superuser_required)
    def get(self, request, *args, **kwargs):
        employers = Employer.objects.all()
        context = {'employers': employers}
        return render(request, self.template_name, context)

def delete_employer(request, employer_id):
    employer = get_object_or_404(Employer, pk=employer_id)
    employer.delete()
    return redirect('employer-list')

class EditEmployerView(View):
    template_name = 'edit_employer.html'
    @method_decorator(superuser_required)
    def get(self, request, employer_id, *args, **kwargs):
        employer = get_object_or_404(Employer, pk=employer_id)
        context = {'employer': employer}
        return render(request, self.template_name, context)

    def post(self, request, employer_id, *args, **kwargs):
        employer = get_object_or_404(Employer, pk=employer_id)
        data = {
            'name': request.POST.get('name'),
            'prenom': request.POST.get('prenom'),
            'telephone': request.POST.get('telephone'),
        }
        try:
            # Mettre à jour les données de l'employeur avec les nouvelles données
            for key, value in data.items():
                setattr(employer, key, value)
            print(request.POST.get("departement"))
            departement_id = employer.departement.id
            depart = get_object_or_404(Departement, pk=departement_id)
            depart.name = request.POST.get("departement")
            depart.save()
            employer.save()
            
            messages.success(request, "Employeur modifié avec succès")
        except Exception as e:
            messages.error(request, f"Problème lors de la modification de l'employeur : {e}")
        return redirect('employer-list')
def delete_employer(request, employer_id):
    employer = get_object_or_404(Employer, pk=employer_id)
    
    try:
        # Delete the employer
        employer.delete()
        messages.success(request, "Employé supprimé avec succès")
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression de l'employé : {e}")
    
    return redirect('employer-list')
    
class addDemandeView(View):
    template_name = 'add.demande.html'

    def get(self, request, *args, **kwargs):
        fournisseurs = Fournisseur.objects.all()
        context = {
            'compte_choices': Compte.TYPE_COMPTE,
            'achat_choices': Compte.TYPE_ACHAT,
            'fournisseurs': fournisseurs,
            'employer': Employer.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        type_compte = request.POST.get('type_compte-1')
        type_achat = request.POST.get('type_achat-1')
        fournisseur_id = request.POST.get('fournisseur-1')
        fournisseur = Fournisseur.objects.get(pk=fournisseur_id)
        employer_id = request.POST.get('employer')
        total = request.POST.get('total')

        if request.POST.get('employer'):
            employer = Employer.objects.get(pk=request.POST.get('employer'))
        else:
            employer = Employer.objects.get(pk=request.user.id)

        demande = Demande.objects.create(
            employer=employer,
            type_compte=type_compte,
            type_achat=type_achat,
            fournisseur=fournisseur,
            total=total,
        )
        demande.save()
        dem = Demande.objects.get(pk=demande.id)
        
        print(demande.id)

        articles = []
        i = 1
        while request.POST.get(f'nom_besoin-{i}'):
            articlename = request.POST.get(f'nom_besoin-{i}')
            quantite = request.POST.get(f'nombre-{i}')
            prix = request.POST.get(f'prix_unitaire-{i}')
            total_article = request.POST.get(f'total-a-{i}')
            print(i)
            if articlename and quantite and prix and total_article:
                article = Article(
                    name=articlename,
                    quantity=quantite,
                    prix_unitaire=prix,
                    total=total_article,
                    employer=employer,
                    demande=dem,
                )
                article.save()
                articles.append(article)
            i += 1

        messages.success(request, "Demande enregistrée avec succès")
        return redirect('add-demande')

from django.shortcuts import render
from django.views import View
import plotly.graph_objects as go

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        
        total_employers = Employer.objects.count()
        total_demandes = Demande.objects.count()
        demande_valide_count = Demande.objects.filter(valider=True).count()
        demande_invalide_count = total_demandes - demande_valide_count

        # Créer les données pour le graphique
        labels = ['Demandes Validées', 'Demandes Invalidées']
        values = [demande_valide_count, demande_invalide_count]

        # Créer le graphique à afficher
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])

        # Personnaliser les couleurs
        fig.update_traces(marker=dict(colors=['#28a745', '#dc3545']))

        # Personnaliser la mise en page
        fig.update_layout(
            title_text='Répartition des Demandes',
            annotations=[dict(text='Demandes', x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=20, r=20, t=40, b=20)
        )

        # Convertir le graphique en HTML
        graph_html = fig.to_html(full_html=False)

        # Passer les statistiques et le graphique au contexte
        context = {
            'total_employers': total_employers,
            'total_demandes': total_demandes,
            'demande_valide_count': demande_valide_count,
            'demande_invalide_count': demande_invalide_count,
            'graph_html': graph_html,
        }
        return render(request, self.template_name, context)

class VisuelDemande(View):
    template_name = 'demande.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = Demande.objects.get(pk=pk)
        
        # Utiliser la relation ForeignKey pour récupérer les articles associés
        articles = Article.objects.filter(demande=obj)
        total_sum = 0
        # Utiliser la fonction sum() pour faire la somme de tous les champs 'total' des articles
        for article in articles:
            total_sum  += article.total
            print(total_sum)
        context = get_demande(pk)
    
        context['total_sum'] = total_sum  # Ajouter la somme totale au contexte

        return render(request, self.template_name, context)

def get_demande_pdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    context = get_demande(pk)

    context['date'] = datetime.datetime.today()
    # Rendre le template HTML
    template = get_template('demande-pdf.html')
    html = template.render(context)

    # Options de format PDF
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # Chemin vers wkhtmltopdf
    path_to_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"  # Remplacez par le chemin correct
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    # Génération du PDF
    try:
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    except OSError as e:
        return HttpResponse(f"Error generating PDF: {e}", content_type="text/plain")

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="demande.pdf"'

    return response
def envoyer_email(request, demande_id):
    demande = get_object_or_404(Demande, id=demande_id)
    articles = Article.objects.filter(demande=demande)  # Obtenir les articles associés
    employer = demande.employer

    client = {
        'nom': 'Niavo Diary',
        'email': 'diaryniavo7@gmail.com',
        'libelle': 'demande d\'achat'
    }

    context = {
        'articles': articles,
        'obj': demande,
        'date': demande.demande_date
    }

    subject = 'Demande d\'achat'
    to = client['email']
    from_email = 'votre_email@example.com'  # Remplacez par votre adresse email

    html_content = render_to_string('demande-pdf.html', context)
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = 'html'

    try:
        msg.send()
        messages.success(request, "Email envoyé avec succès")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'envoi de l'email : {e}")

    return redirect('home')

def user_list_view(request):
        users = User.objects.all()
        print(users)
        context = {'users': users}
        return render(request,"list_user.html", context)


class EditUserView(View):
    template_name = 'edit_user.html'
    @method_decorator(superuser_required)
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        context = {'user': user}
        return render(request, self.template_name, context)

    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirmation')

        if new_password:
            if new_password == confirm_password:
                user.password = make_password(new_password)
            else:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return redirect('edit-user', user_id=user.id)

        try:
            user.save()
            messages.success(request, "Utilisateur modifié avec succès")
        except Exception as e:
            messages.error(request, f"Problème lors de la modification de l'utilisateur : {e}")
        
        return redirect("/user-list")
def delete_user(request, user_id):
    try:
        with transaction.atomic():
            user = User.objects.get(pk=user_id)
            employer = Employer.objects.get(pk=user_id)
            user.delete()
            employer.delete()
            messages.success(request, "Utilisateur et employeur associé supprimés avec succès")
    except Exception as e:
        messages.error(request, f"Problème lors de la suppression de l'utilisateur et de l'employeur associé : {e}")
    
    return redirect("/user-list")
