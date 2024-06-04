# Generated by Django 5.0.6 on 2024-06-04 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0018_remove_demande_article_article_demande'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='type_achat',
            field=models.CharField(choices=[('BR', 'Achat de biens de fonctionnement général'), ('OR', 'Achat de biens à usage spécifique '), ('IN', 'Carburant ou combustibles'), ('SR', 'Internet'), ('AU', 'Autre achat')], max_length=2),
        ),
        migrations.AlterField(
            model_name='demande',
            name='type_achat',
            field=models.CharField(choices=[('BR', 'Achat de biens de fonctionnement général'), ('OR', 'Achat de biens à usage spécifique '), ('IN', 'Carburant ou combustibles'), ('SR', 'Internet'), ('AU', 'Autre achat')], default='BR', max_length=2),
        ),
    ]
