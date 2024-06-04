# Generated by Django 5.0.4 on 2024-05-11 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0006_remove_article_fournisseur_demande_fournisseur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande',
            name='article',
        ),
        migrations.AddField(
            model_name='demande',
            name='article_name',
            field=models.CharField(default=1, max_length=135),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demande',
            name='article_quantite',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demande',
            name='article_unit_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=1000),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
