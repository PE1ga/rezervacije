# Generated by Django 4.1.5 on 2023-01-14 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplikacija', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='graf',
            name='S20',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='graf',
            name='S21',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='graf',
            name='S22',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='graf',
            name='S23',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='graf',
            name='S24',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='graf',
            name='S25',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='graf',
            name='S26',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='graf',
            name='S27',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='vnosgostov',
            name='OdpovedDne',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vnosgostov',
            name='RokPlacilaAvansa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vnosgostov',
            name='do',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vnosgostov',
            name='od',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vnosgostov',
            name='sifravnosa',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Šifra vnosa'),
        ),
    ]
