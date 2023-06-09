# Generated by Django 4.1.5 on 2023-02-13 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VnosGostov',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datumvnosa', models.CharField(blank=True, max_length=30, null=True)),
                ('sifravnosa', models.CharField(blank=True, max_length=100, null=True, verbose_name='Šifra vnosa')),
                ('imestranke', models.CharField(max_length=100, verbose_name='Ime Stranke')),
                ('agencija', models.CharField(max_length=100, verbose_name='Agencija')),
                ('od', models.CharField(max_length=100)),
                ('do', models.CharField(max_length=100)),
                ('dniPredr', models.IntegerField(blank=True, default=0, null=True)),
                ('CENA', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cena')),
                ('stsobe', models.IntegerField()),
                ('SO', models.IntegerField()),
                ('tip', models.CharField(max_length=100)),
                ('RNA', models.CharField(max_length=100)),
                ('AvansEUR', models.IntegerField(blank=True, default=0, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('DR', models.CharField(max_length=100)),
                ('zahteve', models.TextField(blank=True, null=True)),
                ('Alergije', models.CharField(blank=True, max_length=100, null=True)),
                ('Mes_Let', models.CharField(blank=True, max_length=100, null=True)),
                ('Noc_SK', models.IntegerField(blank=True, null=True)),
                ('StanjeTTAX', models.CharField(blank=True, max_length=100, null=True)),
                ('OdpRok', models.IntegerField(blank=True, null=True)),
                ('IDponudbe', models.IntegerField(blank=True, null=True)),
                ('RokPlacilaAvansa', models.CharField(blank=True, max_length=100, null=True)),
                ('Zaklenjena', models.CharField(blank=True, max_length=100, null=True)),
                ('OdpovedDne', models.CharField(blank=True, max_length=100, null=True)),
                ('SOTR', models.IntegerField(blank=True, default=0, null=True)),
                ('SOMAL', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AddIndex(
            model_name='vnosgostov',
            index=models.Index(fields=['-id'], name='Rezervacije_id_66ac7d_idx'),
        ),
    ]
