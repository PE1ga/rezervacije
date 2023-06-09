# Generated by Django 4.1.5 on 2023-03-08 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0008_alter_ponudba_avans'),
    ]

    operations = [
        migrations.AddField(
            model_name='ponudba',
            name='datumPotrditve',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='dodatnoLezisce',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='jezik',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='multiroom',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='odpRok',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='rokPlacilaAvansa',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='skiCenaSkiInNast',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='skiOsebe',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='skiXXdn',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='sklic',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='stNocitev',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ponudba',
            name='zahteve',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
