# Generated by Django 4.1.5 on 2023-02-28 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0003_alter_vnosgostov_noc_sk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vnosgostov',
            name='od',
            field=models.DateField(),
        ),
    ]
