# Generated by Django 5.0.6 on 2024-06-01 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0012_remove_demande_articles_demande_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande',
            name='article',
        ),
        migrations.AlterField(
            model_name='article',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fact_app.demande'),
        ),
    ]
