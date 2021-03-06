# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-26 13:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrivage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('date_arrivee', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_no', models.PositiveSmallIntegerField(blank=True, help_text='no de la prise de vue', null=True, unique=True)),
                ('type_client', models.CharField(choices=[('H', 'Homme'), ('F', 'Femme'), ('M', 'Mixte'), ('E', 'Enfant')], default='F', max_length=1)),
                ('genre_article', models.CharField(choices=[('A', 'Accessoire'), ('V', 'Vêtement'), ('C', 'Chaussure'), ('S', 'Sous-vêtement')], default='S', max_length=1)),
                ('nom', models.CharField(default='ensemble', max_length=100)),
                ('quantite', models.IntegerField(default=1)),
                ('prix_unitaire', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('prix_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('remise', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('date_ajout', models.DateField(auto_now_add=True)),
                ('couleurs_quantites', models.CharField(blank=True, max_length=200, null=True)),
                ('motifs', models.CharField(blank=True, max_length=200, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('type_taille', models.CharField(blank=True, choices=[('1', 'EUR'), ('2', 'US'), ('3', 'UK')], default='1', max_length=1, null=True)),
                ('taille', models.CharField(blank=True, choices=[('1', 'S'), ('2', 'M'), ('3', 'L'), ('4', 'XL'), ('5', 'XXL'), ('6', 'XXXL'), ('7', 'XXXXL'), ('8', '5XL'), ('9', '6XL'), ('10', '7XL'), ('11', '8XL')], max_length=2, null=True)),
                ('taille_nombre', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('local', models.CharField(default='bas', max_length=20)),
                ('solde', models.CharField(choices=[('N', '-'), ('S', 'en solde')], default='N', max_length=1)),
                ('ventes', models.CharField(blank=True, help_text='25000, 35000', max_length=200, null=True)),
                ('tailles_vendues', models.CharField(blank=True, help_text='(XL, 1), (M, 2)', max_length=200, null=True)),
                ('arrivage', models.ForeignKey(blank=True, default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Arrivage')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Frais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=20)),
                ('objet', models.TextField()),
                ('date', models.DateField()),
                ('arrivage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Arrivage')),
                ('entreprise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Enterprise')),
            ],
            options={
                'verbose_name_plural': 'Frais',
            },
        ),
        migrations.CreateModel(
            name='Marque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='articles')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Article')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='enterprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='inventory.Enterprise'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='entreprise',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='inventory.Enterprise'),
        ),
        migrations.AddField(
            model_name='article',
            name='marque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Marque'),
        ),
        migrations.AddField(
            model_name='arrivage',
            name='proprietaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.Enterprise'),
        ),
    ]
