# Generated by Django 4.1.5 on 2023-02-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplikacija', '0007_graf_s28'),
    ]

    operations = [
        migrations.AddField(
            model_name='pospravljanjeprihodi',
            name='ok1',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='pospravljanjeprihodi',
            name='ok2',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='pospravljanjeprihodi',
            name='ok3',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='pospravljanjeprihodi',
            name='ok4',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
