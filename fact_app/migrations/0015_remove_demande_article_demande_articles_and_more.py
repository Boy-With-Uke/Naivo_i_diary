# Generated by Django 5.0.6 on 2024-06-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fact_app', '0014_demande_article_alter_article_employer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande',
            name='article',
        ),
        migrations.AddField(
            model_name='demande',
            name='articles',
            field=models.ManyToManyField(related_name='demandes', to='fact_app.article'),
        ),
        migrations.AlterField(
            model_name='compte',
            name='type_achat',
            field=models.CharField(choices=[('BR', 'Bureau'), ('OR', 'Ordinateur'), ('IN', 'Internet'), ('SR', 'Service')], max_length=2),
        ),
        migrations.AlterField(
            model_name='demande',
            name='type_achat',
            field=models.CharField(choices=[('BR', 'Bureau'), ('OR', 'Ordinateur'), ('IN', 'Internet'), ('SR', 'Service')], default='BR', max_length=2),
        ),
    ]
