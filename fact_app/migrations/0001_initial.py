# Generated by Django 5.0.4 on 2024-05-10 13:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_compte', models.CharField(choices=[('ADB', 'Achats de biens'), ('ASC', 'Achats de services et charges permanentes')], max_length=3)),
                ('type_achat', models.CharField(choices=[('BR', 'Burreau'), ('OR', 'Ordinateur'), ('IN', 'Internet'), ('SR', 'Service')], max_length=2)),
            ],
            options={
                'verbose_name': 'Compte',
                'verbose_name_plural': 'Comptes',
            },
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=132)),
                ('prenom', models.CharField(max_length=132)),
                ('telephone', models.CharField(max_length=10)),
                ('departement', models.CharField(max_length=132)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Employer',
                'verbose_name_plural': 'Employers',
            },
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demande_date', models.DateTimeField(auto_now_add=True)),
                ('type_compte', models.CharField(choices=[('ADB', 'Achats de biens'), ('ASC', 'Achats de services et charges permanentes')], default='ADB', max_length=3)),
                ('type_achat', models.CharField(choices=[('BR', 'Burreau'), ('OR', 'Ordinateur'), ('IN', 'Internet'), ('SR', 'Service')], default='BR', max_length=2)),
                ('last_update', models.DateTimeField(null=True)),
                ('valider', models.BooleanField(default=False)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('achat', models.CharField(max_length=32, null=True)),
                ('quantite', models.IntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fact_app.employer')),
            ],
            options={
                'verbose_name': 'Demande',
                'verbose_name_plural': 'Demandes',
            },
        ),
    ]
