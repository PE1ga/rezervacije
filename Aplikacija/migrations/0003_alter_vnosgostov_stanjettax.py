# Generated by Django 4.1.5 on 2023-01-15 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplikacija', '0002_graf_s20_graf_s21_graf_s22_graf_s23_graf_s24_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vnosgostov',
            name='StanjeTTAX',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
