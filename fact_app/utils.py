from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)

from .models import *

def pagination(request, demandes):
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

        return items_page


def get_demande(pk):
   
    obj = Demande.objects.get(pk=pk)
    articles = Article.objects.filter(employer=obj.employer)
       
    context = {
        'obj':obj,
        'articles': articles
     }
    return context