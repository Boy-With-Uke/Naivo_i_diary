from django.db import models
from compte.models import User

class Compte(models.Model):
    TYPE_COMPTE = (
        ('ADB', 'Achats de biens'),
        ('ASC', 'Achats de services et charges permanentes'),
    )
    type_compte = models.CharField(max_length=3, choices=TYPE_COMPTE)
    TYPE_ACHAT =(
        ('BR', 'Achat de biens de fonctionnement général'),
        ('OR', 'Achat de biens à usage spécifique '),
        ('IN','Carburant ou combustibles'),
        ('SR','Internet'),
        ('AU', 'Autre achat'),
    )
    type_achat = models.CharField(max_length=2,choices=TYPE_ACHAT)

    class Meta:
        verbose_name = 'Compte'
        verbose_name_plural = 'Comptes'

    def __str__(self):
        return self.get_type_compte_display()
    def __str__(self) :
        return self.get_type_achat_display()
    
class Departement(models.Model):
    name = models.CharField(max_length=132)

    class Meta:
        verbose_name = "Departement"
        verbose_name_plural = "Departements"
    def __str__ (self):
        return self.name
    
class Fournisseur(models.Model):
    name = models.CharField(max_length=132)
    email = models.EmailField()
    addresse = models.CharField(max_length=132)

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
    def __str__(self) :
        return self.name
    
class Employer(models.Model):
    name = models.CharField(max_length=132)
    prenom = models.CharField(max_length=132)
    telephone = models.CharField(max_length=10)
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Employer"
        verbose_name_plural = "Employers"
        
    def __str__(self):
        return self.name
    
   


   



class Demande(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT)
    demande_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(null=True)
    valider = models.BooleanField(default=False)
    commentaire = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=10000, decimal_places=2)
    type_compte = models.CharField(max_length=3, choices=Compte.TYPE_COMPTE, default='ADB')
    type_achat = models.CharField(max_length=2, choices=Compte.TYPE_ACHAT, default='BR')
    total = models.DecimalField(max_digits=100000000000000, decimal_places=2, null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "Demande"
        verbose_name_plural = "Demandes"
        
    def __str__(self):
        return f"{self.employer.name}_{self.demande_date}"
    
    @property
    def get_total(self):
        articles = self.article_set.all()
        total = sum(article.get_total for article in articles)
        return total
    
    def get_type_compte_content(self):
        return dict(Compte.TYPE_COMPTE)[self.type_compte]
    
class Article(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    name = models.CharField(max_length=135)
    quantity = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=1000, decimal_places=2)
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    
    
    total = models.DecimalField(max_digits=1000, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total(self):
        total = self.quantity * self.prix_unitaire
        return total

  