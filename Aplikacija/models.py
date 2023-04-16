from django.db import models

"""
class Members(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

class GostiSeznam(models.Model):
    Ime = models.CharField(max_length= 255)
    Agencija = models.CharField(max_length= 255)
    Cena = models.CharField(max_length= 255)
    DatumOD = models.CharField(max_length= 255)
    DatumDO = models.CharField(max_length= 255)
"""

class ObravnavaniDatum(models.Model):
    Naziv = models.CharField(max_length=25)
    DatumObravnavani = models.CharField(max_length=25)


class Pospravljanje(models.Model):
    choicesStSob=[(10,10),(20,20)]
    choicesAgen=[("",""),("BookingCom","BookingCom"),("Siteminder","Siteminder")]
    
    Soba = models.IntegerField(choices=choicesStSob, default="10")
    Akcija = models.CharField(max_length=20)
    Za_Oseb = models.IntegerField()
    Status = models.CharField(max_length=20)
    
    DatumVnosa = models.CharField(max_length= 20)
    Ime = models.CharField(max_length= 25)
    Agencija = models.CharField(max_length= 20, choices=choicesAgen, default="")
    Od = models.CharField(max_length= 20)
    Do = models.CharField(max_length= 20)
    Cena = models.CharField(max_length= 20)
    Oseb = models.CharField(max_length= 20)
    Tip = models.CharField(max_length= 20)
    Drzava = models.CharField(max_length= 255)
    Zahteve = models.CharField(max_length= 254, null=True)
    Alergije = models.CharField(max_length= 25)
    RNA = models.CharField(max_length=20)
    StatusZajtrk= models.CharField(max_length=20)


class PospravljanjePrihodi(models.Model):
    Soba = models.IntegerField()
    St_Oseb = models.IntegerField()
    #Zahteve = models.CharField(max_length=255)
    Status = models.CharField(max_length=20)
    StatusCheckIn = models.CharField(max_length=20, null=True)
    DatumVnosa = models.CharField(max_length= 20)
    Ime = models.CharField(max_length= 25)
    Agencija = models.CharField(max_length= 20)
    Od = models.CharField(max_length= 20)
    Do = models.CharField(max_length= 20)
    Cena = models.CharField(max_length= 20)
    Tip = models.CharField(max_length= 20)
    Drzava = models.CharField(max_length= 255)
    Zahteve = models.CharField(max_length= 254, null=True)
    Alergije = models.CharField(max_length= 25)
    RNA = models.CharField(max_length=20)
    Ttax = models.CharField(max_length=45, null=True)
    ok1 = models.CharField(max_length=45, null=True)
    ok2 = models.CharField(max_length=45, null=True)
    ok3 = models.CharField(max_length=45, null=True)
    ok4 = models.CharField(max_length=45, null=True)
    

class Graf(models.Model):
    S0 = models.CharField(max_length= 20, null=True)
    S1 = models.CharField(max_length= 20, null=True)
    S2 = models.CharField(max_length= 20, null=True)
    S3 = models.CharField(max_length= 20, null=True)
    S4 = models.CharField(max_length= 20, null=True)
    S5 = models.CharField(max_length= 20, null=True)
    S6 = models.CharField(max_length= 20, null=True)
    S7 = models.CharField(max_length= 20, null=True)
    S8 = models.CharField(max_length= 20, null=True)
    S9 = models.CharField(max_length= 20, null=True)
    S10 = models.CharField(max_length= 20, null=True)
    S11 = models.CharField(max_length= 20, null=True)
    S12 = models.CharField(max_length= 20, null=True)
    S13 = models.CharField(max_length= 20, null=True)
    S14 = models.CharField(max_length= 20, null=True)
    S15 = models.CharField(max_length= 20, null=True)
    S16 = models.CharField(max_length= 20, null=True)
    S17 = models.CharField(max_length= 20, null=True)
    S18 = models.CharField(max_length= 20, null=True)
    S19 = models.CharField(max_length= 20, null=True)
    S20 = models.CharField(max_length= 20, null=True)
    S21 = models.CharField(max_length= 20, null=True)
    S22 = models.CharField(max_length= 20, null=True)
    S23 = models.CharField(max_length= 20, null=True)
    S24 = models.CharField(max_length= 20, null=True)
    S25 = models.CharField(max_length= 20, null=True)
    S26 = models.CharField(max_length= 20, null=True)
    S27 = models.CharField(max_length= 20, null=True)
    S28 = models.CharField(max_length= 20, null=True)

    objects = models.Manager()

class PrazneSobe(models.Model):
    Soba = models.IntegerField()
    NaslPrh = models.CharField(max_length= 20)
    DniDoPrih = models.CharField(max_length= 10)

class CheckLista(models.Model):
    Akcija = models.CharField(max_length=255)
    Status = models.CharField(max_length=10)
    



class ChListSobaID(models.Model):
    Opis = models.CharField(max_length=20)
    SobaID = models.CharField(max_length=30)
    StSobe = models.IntegerField()
    VseOK = models.CharField(max_length=10)




# TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST
"""
class VnosGostov(models.Model):
    datumvnosa = models.CharField(max_length=30, null=True, blank=True)  #models.DateField(auto_now_add=True)
    sifravnosa	= models.CharField(verbose_name="Šifra vnosa", max_length=100, null=True, blank=True)
    imestranke	= models.CharField(verbose_name="Ime Stranke", max_length=100)
    agencija	= models.CharField(verbose_name="Agencija", max_length=100)
    od = models.CharField(max_length=100) #models.DateField(verbose_name="Datum OD")
    do = models.CharField(max_length=100)#models.DateField(verbose_name="Datum DO")
    dniPredr = models.IntegerField(null=True, blank=True)
    CENA = models.DecimalField(verbose_name="Cena", decimal_places=2, max_digits=10)
    stsobe = models.IntegerField()
    SO	= models.IntegerField()
    tip	= models.CharField(max_length=100)
    RNA = models.CharField(max_length=100)
    AvansEUR = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    DR	= models.CharField(max_length=100)
    zahteve = models.TextField(null=True, blank=True )
    Alergije = models.CharField(max_length=100, null=True, blank=True)
    Mes_Let	= models.CharField(max_length=100, null=True, blank=True)
    Noc_SK = models.IntegerField(null=True, blank=True)
    StanjeTTAX = models.CharField(max_length=100, null=True, blank=True)
    OdpRok = models.IntegerField(null=True, blank=True)
    IDponudbe = models.IntegerField(null=True, blank=True)
    RokPlacilaAvansa =models.CharField(max_length=100,null=True, blank=True) #models.DateField(null=True, blank=True)
    Zaklenjena = models.CharField(max_length=100, null=True, blank=True)
    OdpovedDne= models.CharField(max_length=100,null=True, blank=True)     #models.DateField(null=True, blank=True)
    SOTR= models.IntegerField(null=True, blank=True)
    SOMAL= models.IntegerField(null=True, blank=True)

    
    def __str__(self):
        return self.imestranke
"""