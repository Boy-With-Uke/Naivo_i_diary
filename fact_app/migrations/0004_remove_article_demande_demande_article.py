# Generated by Django 5.0.4 on 2024-05-11 22:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0003_departement_fournisseur_remove_demande_achat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='demande',
        ),
        migrations.AddField(
            model_name='demande',
            name='article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fact_app.article'),
            preserve_default=False,
        ),
    ]
