# Generated by Django 4.1.5 on 2023-03-08 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0007_alter_ponudba_stotr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ponudba',
            name='avans',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
