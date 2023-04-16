# Generated by Django 4.1.5 on 2023-04-09 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Rezervacije', '0020_bar_narocila_kolicina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vnosgostov',
            name='Noc_SK',
        ),
        migrations.AddField(
            model_name='vnosgostov',
            name='cena_nocitve',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10, verbose_name='Cena nočitve'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vnosgostov',
            name='nocitev_skupaj',
            field=models.IntegerField(default=0, verbose_name='Nočitev skupaj'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bar_narocila',
            name='artikel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Rezervacije.bar_cenik'),
        ),
        migrations.AlterField(
            model_name='bar_narocila',
            name='gost',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Rezervacije.vnosgostov'),
        ),
    ]
