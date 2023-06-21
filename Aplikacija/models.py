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

    objects = models.Manager()


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
    ok1 = models.CharField(max_length=45, null=True)
    ok2 = models.CharField(max_length=45, null=True)
    ok3 = models.CharField(max_length=45, null=True)
    ok4 = models.CharField(max_length=45, null=True)
    cas_ciscenja = models.DateTimeField(null=True)
    uni_koda = models.CharField(max_length= 20, null= True)
    cas_zajtrka = models.DateTimeField(null=True)
    status_zajtrk_num = models.IntegerField(null=True)
    status_num = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        if self.StatusZajtrk =="OK":
            self.status_zajtrk_num= 1
        else:
            self.status_zajtrk_num= None
        
        if self.Status == "NE CISTI!":
            self.status_num = 1
        elif self.Status == "OK" or self.Status == "KO":
            self.status_num = 2
        else:
            self.status_num = None

        
        
        super(Pospravljanje, self).save(*args, **kwargs)



    objects = models.Manager()

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
    uni_koda = models.CharField(max_length= 20, null= True)
    cas_checkin = models.DateTimeField(null=True)
    st_noci = models.IntegerField(null=True)
    
    objects = models.Manager()



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

    objects = models.Manager()

class CheckLista(models.Model):
    Akcija = models.CharField(max_length=255)
    Status = models.CharField(max_length=10)
    #Soba = models.IntegerField()
    #Akcija1 =  models.CharField(max_length=20)
    #Akcija2 =  models.CharField(max_length=20)
    #Akcija3 =  models.CharField(max_length=20)
    #Akcija4 =  models.CharField(max_length=20)
    #Akcija5 =  models.CharField(max_length=20)
    #Akcija6 =  models.CharField(max_length=20)
    #Akcija7 =  models.CharField(max_length=20)
    #Akcija8 =  models.CharField(max_length=20)
    #Akcija9 =  models.CharField(max_length=20)
    #Akcija10=  models.CharField(max_length=20)

    objects = models.Manager()






class ChListSobaID(models.Model):
    Opis = models.CharField(max_length=20)
    SobaID = models.CharField(max_length=30)
    StSobe = models.IntegerField()
    VseOK = models.CharField(max_length=10)

    objects = models.Manager()

