# Generated by Django 4.1.5 on 2023-02-02 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplikacija', '0006_delete_vnosgostov'),
    ]

    operations = [
        migrations.AddField(
            model_name='graf',
            name='S28',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
