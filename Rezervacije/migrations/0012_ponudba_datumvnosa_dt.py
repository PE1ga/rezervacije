# Generated by Django 4.1.5 on 2023-03-27 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0011_alter_ponudba_options_alter_ponudba_zahteve_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ponudba',
            name='datumVnosa_dt',
            field=models.DateTimeField(null=True),
        ),
    ]
