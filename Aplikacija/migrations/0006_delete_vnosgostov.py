# Generated by Django 4.1.5 on 2023-01-30 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aplikacija', '0005_alter_vnosgostov_datumvnosa'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VnosGostov',
        ),
    ]
