# Generated by Django 4.1.5 on 2023-03-10 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0009_ponudba_datumpotrditve_ponudba_dodatnolezisce_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ponudba',
            name='stSob',
        ),
    ]