from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class VnosGostov(models.Model):
    datumvnosa = models.CharField(max_length=30, null=True, blank=True)  #models.DateField(auto_now_add=True)
    sifravnosa	= models.CharField(verbose_name="Šifra vnosa", max_length=100, null=True, blank=True)
    imestranke	= models.CharField(verbose_name="Ime Stranke", max_length=100)
    agencija	= models.CharField(verbose_name="Agencija", max_length=100)
    od = models.CharField(max_length=100) #models.DateField(verbose_name="Datum OD")
    do = models.CharField(max_length=100)#models.DateField(verbose_name="Datum DO")
    dniPredr = models.IntegerField(null=True, blank=True, default=0)
    CENA = models.DecimalField(verbose_name="Cena", decimal_places=2, max_digits=10)
    cena_nocitve = models.DecimalField(verbose_name="Cena nočitve", null=True, blank=True, decimal_places=4, max_digits=10)
    stsobe = models.IntegerField()
    SO	= models.IntegerField()
    tip	= models.CharField(max_length=100)
    RNA = models.CharField(max_length=100)
    AvansEUR = models.IntegerField(null=True, blank=True, default=0)
    email = models.EmailField(null=True, blank=True)
    DR	= models.CharField(max_length=100)
    zahteve = models.TextField(null=True, blank=True )
    Alergije = models.CharField(max_length=100, null=True, blank=True)
    Mes_Let	= models.CharField(max_length=100, null=True, blank=True)
    nocitev_skupaj = models.IntegerField(verbose_name="Nočitev skupaj", null=True, blank=True)
    st_noci = models.IntegerField(verbose_name="Noči skupaj", null=True, blank=True)
    StanjeTTAX = models.CharField(max_length=100) #, null=True, blank=True)
    OdpRok = models.IntegerField(null=True, blank=True)
    IDponudbe = models.CharField(max_length=20, null=True, blank=True)
    RokPlacilaAvansa =models.CharField(max_length=100,null=True, blank=True) #models.DateField(null=True, blank=True)
    Zaklenjena = models.CharField(max_length=100, null=True, blank=True)
    OdpovedDne= models.CharField(max_length=100,null=True, blank=True)     #models.DateField(null=True, blank=True)
    SOTR= models.IntegerField(null=True, blank=True, default=0)
    SOMAL= models.IntegerField(null=True, blank=True, default=0)
    status_rez = models.CharField(max_length=100)
    
    datumVnosa_dt = models.DateTimeField(null=True)
    od_dt= models.DateTimeField(null=True)
    do_dt= models.DateTimeField(null=True)

    objects = models.Manager()
    
    
    def save(self, *args, **kwargs):
        if self.datumvnosa:
            self.datumVnosa_dt= datetime.strptime(self.datumvnosa, "%d.%m.%Y")
        if self.od:
            self.od_dt= datetime.strptime(self.od, "%d.%m.%Y")
        if self.do:
            self.do_dt= datetime.strptime(self.do, "%d.%m.%Y")
        
        super(VnosGostov, self).save(*args, **kwargs)
    







    class Meta:  # podatke, ki jih boš dobil v queryset bodo sortirani descend po IDju
        ordering= ["-id"]
        indexes =[
            models.Index(fields=["-id"])
        ]


    """def __str__(self):
        return self.imestranke"""
class Ponudba(models.Model):
    datumVnosa= models.CharField(max_length=30, null=True, blank=True) 
    status = models.CharField(max_length=30, null=True, blank=True) 
    ime = models.CharField(max_length=30, null=True, blank=True) 
    od = models.CharField(max_length=30, null=True, blank=True) 
    do = models.CharField(max_length=30, null=True, blank=True) 
    email = models.CharField(max_length=30, null=True, blank=True) 
    rna = models.CharField(max_length=30, null=True, blank=True) 
    avans = models.IntegerField(null=True, blank=True)
    odpoved = models.IntegerField()
    stOdr = models.IntegerField()
    stOtr = models.CharField(max_length=30, null=True, blank=True) 
    tip = models.CharField(max_length=30, null=True, blank=True) 
    cena = models.IntegerField()
    odpRok= models.CharField(max_length=30, null=True, blank=True)
    jezik= models.CharField(max_length=30, null=True, blank=True)
    multiroom= models.CharField(max_length=30, null=True, blank=True)
    datumPotrditve= models.CharField(max_length=30, null=True, blank=True)
    sklic= models.CharField(max_length=30, null=True, blank=True)
    zahteve= models.CharField(max_length=255, null=True, blank=True)
    stNocitev= models.CharField(max_length=30, null=True, blank=True)
    dodatnoLezisce= models.CharField(max_length=30, null=True, blank=True)
    rokPlacilaAvansa= models.CharField(max_length=30, null=True, blank=True)
    skiXXdn= models.CharField(max_length=30, null=True, blank=True)
    skiOsebe= models.CharField(max_length=30, null=True, blank=True)
    skiCenaSkiInNast= models.CharField(max_length=30, null=True, blank=True)

    datumVnosa_dt = models.DateTimeField(null=True)
    od_dt= models.DateTimeField(null=True)
    do_dt= models.DateTimeField(null=True)

    objects = models.Manager()
    
    
    def save(self, *args, **kwargs):
        if self.datumVnosa:
            self.datumVnosa_dt= datetime.strptime(self.datumVnosa, "%d.%m.%Y")
        if self.od:
            self.od_dt= datetime.strptime(self.od, "%d.%m.%Y")
        if self.do:
            self.do_dt= datetime.strptime(self.do, "%d.%m.%Y")
        
        super(Ponudba, self).save(*args, **kwargs)
    
    
    class Meta:  # podatke, ki jih boš dobil v queryset bodo sortirani descend po IDju
        ordering= ["-id"]
        indexes =[
            models.Index(fields=["-id"])]



class Bar_cenik(models.Model):
    opis = models.CharField(verbose_name="Opis", max_length=255)
    cena = models.DecimalField(verbose_name="Cena", decimal_places=4, max_digits=10)
    #kolicina = models.IntegerField(verbose_name="Količina")
    enota = models.CharField(max_length=10)
    ddv = models.DecimalField(verbose_name="DDV", decimal_places=2, max_digits=10)
    #bruto_z_ddv = models.DecimalField(verbose_name="Bruto cena z ddv", decimal_places=2, max_digits=10)
    #bruto_suma_z_ddv =  models.DecimalField(verbose_name="Bruto cena z ddv", decimal_places=2, max_digits=10)

    objects = models.Manager()

    def __str__(self):
        return self.opis


class Bar_narocila(models.Model):
    artikel = models.ForeignKey(Bar_cenik, on_delete=models.SET_NULL, null=True)
    gost = models.ForeignKey(VnosGostov, on_delete=models.SET_NULL, null=True)
    kdaj = models.DateTimeField(auto_now_add=True)
    kolicina = models.IntegerField()

    objects = models.Manager()
    
    def __str__(self):
        return self.artikel.opis


























class SifrantSob(models.Model):
    SifraSobe = models.IntegerField()
    TipSobe = models.CharField(max_length=10)
    StOSeb = models.IntegerField()

    objects = models.Manager()