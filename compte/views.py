from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.views import View


from fact_app.models import Demande

User = get_user_model()

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)

        login(request, user)
        return redirect('login')  # Redirection vers l'URL 'interface' après l'inscription
    return render(request, 'signup.html')


class Inter(View): 
    template_name = 'interface.html'

    def get(self, request, *args, **kwargs):
        demandes = Demande.objects.select_related('employer').all()
        context = {'demandes': demandes}
        return render(request, self.template_name, context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            if request.user.is_superuser:
                return redirect('home')
            else:
                return redirect('interface')
        

    return render(request,'login.html')
def logout_user(request):
    logout(request)
    return redirect('login')

