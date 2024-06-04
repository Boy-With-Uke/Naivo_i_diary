from django.urls import path
from compte.views import login_user, logout_user, signup, Inter
from django.contrib.auth import views as auth_views
from .views import VisuelDemande, user_list_view, EditUserView, delete_user, envoyer_email


from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('add-employer/', views.AddEmployerView.as_view(), name='add-employer'),
    path('employer-list/', views.EmployerListView.as_view(), name='employer-list'),
    path('delete-employer/<int:employer_id>/', views.delete_employer, name='delete-employer'),
    path('edit-employer/<int:employer_id>/', views.EditEmployerView.as_view(), name='edit-employer'),
    path('add-demande/', views.addDemandeView.as_view(), name='add-demande'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('view-demande/<int:pk>/', views.VisuelDemande.as_view(), name='view-demande'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name='logout'),
    path('', login_user, name='login'),
    path('interface/', Inter.as_view(), name='interface'),
    path('demande-pdf/<int:pk>/', views.get_demande_pdf,name="demande-pdf"),
    path('envoyer_email/<int:demande_id>/',envoyer_email, name='envoyer_email'),
    path('user-list/', user_list_view, name='user-list'), 
    path('users/edit/<int:user_id>/', EditUserView.as_view(), name='edit-user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete-user'),

    
]
