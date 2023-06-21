from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast

import json
import os
from datetime import datetime, timedelta, time



#from .forms import VnosRezForm, UpdateRezForm



# Create your views here.

L_2posteljneSobe = [10,11,12,20,21,30,31,32,34,35,36,37,38,39,43,45,46,50,51]
L_4posteljneSobe = [33,41,42,40,44,52]

def index(request):
    ObDatum = ObravnavaniDatum.objects.filter(Naziv="Ime").first()
    #ObDatum = ObravnavaniDatum.objects.get(id=1)
    Ime = "Peter"

    template = loader.get_template("index.html")

    kontext = {"VstaviIme": Ime, "ObDatum": ObDatum}

    return HttpResponse(template.render(kontext, request))


# POSPRAVLJANJE


def PospravljanjeSob(request):
    # CHECKLISTA ####
    # Izbriši vse OK v tabeli Checklista
    CheckLista.objects.all().update(Status="")
    
    ##################
    
    ObDatum = ObravnavaniDatum.objects.filter(Naziv="Ime").first()
    #ObDatum = ObravnavaniDatum.objects.get(id=1)

    #### Po 12 uri odstrani status "ŠLI VEN" , da ne moti čistilk
    trenutni_cas = datetime.now().time()
    cas_1200 = time(12, 00)
    if trenutni_cas > cas_1200:
        Pospravljanje.objects.filter(Status = "ŠLI VEN").update(Status = "")
    ####
     
         
    sobe = Pospravljanje.objects.all().values().order_by("status_num")
    StSob = (sobe.count() -
             sobe.filter(Status="OK").count() -
             sobe.filter(Status="KO").count() -
            sobe.filter(Status="NE CISTI!").count())
    st_sob_ne_cisti = sobe.filter(Status= "NE CISTI!").count()
    
    # Iskanje zadnje očiščene sobe:
    zadnja_ociscena_soba = sobe.order_by("-cas_ciscenja").first()
    st_sobe_zadnje_ocisc = zadnja_ociscena_soba["Soba"]
    # Na začetku še nobena soba ne bo očiščena, zato ne smo biti nobena označena - variabli dam vrednost št sobe= 0:
    
    if zadnja_ociscena_soba["cas_ciscenja"] == None:
        st_sobe_zadnje_ocisc = 0
    
    if "btn_reset" in request.POST:
        zadnja_ociscena_soba = Pospravljanje.objects.order_by("-cas_ciscenja").first()
        zadnja_ociscena_soba.Status = ""
        zadnja_ociscena_soba.cas_ciscenja = None
        zadnja_ociscena_soba.ok1 = None
        zadnja_ociscena_soba.ok2 = None
        zadnja_ociscena_soba.ok3 = None
        zadnja_ociscena_soba.ok4 = None
        zadnja_ociscena_soba.save()
        
    
    # Ugotovi, koliko sobPrihodi je potrebno še pregledati - ta podatek
    prihodi = PospravljanjePrihodi.objects.filter(Status="OK").count()
    stVsehSobPrih = PospravljanjePrihodi.objects.all().count()
    seSobPrihZaPreveriti = stVsehSobPrih - prihodi - PospravljanjePrihodi.objects.filter(
        Status="KO").count()
    template = loader.get_template("pospravljanje.html")
    context = {
        "SobeSeznam": sobe,
        "STSOB": StSob,
        "st_sob_ne_cisti": st_sob_ne_cisti,
        "ObDatum": ObDatum,
        "SeSobPrih": seSobPrihZaPreveriti,
        "DvoPosteljneSobe": L_2posteljneSobe,   # List je na vrhu tega file
        "StiriPosteljneSobe": L_4posteljneSobe,
        "st_sobe_zadnje_ocisc":st_sobe_zadnje_ocisc,
        "list_ok_ko": ["OK", "KO"]
        }
   # Pošlji email, da so vsi PRIHODI POSPRAVLJENI
    # JSON
   
    JS_file = os.path.join(settings.BASE_DIR, 'Aplikacija//static//json//jsonFILE_Pospravljanje.json')
    
    if StSob == 0:
        with open(JS_file, "r", encoding="utf-8") as f:
            json_file = json.load(f)
        if "VseSobeOK" in json_file:
            pass
        else:
            send_mail(subject="POSPRAVLJANJE ZAKLJUČENO", 
                message="Čistilke so POSPRAVILE vse sobe", from_email=settings.EMAIL_HOST_USER, recipient_list=[settings.RECIPIENT_ADDRESS,]
                    )
        
            # v Json shrani list z informacijo, da so vse sobe OK
            with open(JS_file, "w", encoding="utf-8") as f:
                    json.dump(["VseSobeOK"], f, ensure_ascii=False, indent=4)
        
    else:
        # v Json shrani list z informacijo, da vse sobe ni OK
        with open(JS_file, "w", encoding="utf-8") as f:
                json.dump(["VseSobeNIOK"], f, ensure_ascii=False, indent=4)
    
    return HttpResponse(template.render(context, request))

def vpras_pred_potrd_posp(request, id):
    record = Pospravljanje.objects.get(id=id)
    template = loader.get_template("form_vprasaj_pospr.html")
    context = {"soba": record}

    return HttpResponse(template.render(context, request))




def PotrdiCiscenje(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.Status = "OK"
    record.cas_ciscenja = datetime.now()
    record.save()

    # Če ima ta soba tudi prihod, moraš tudi v PospravljanjePrihodi tej sobi sprementiti status v OK
    StSobe = record.Soba
    try:
        recordPrihod = PospravljanjePrihodi.objects.get(Soba=StSobe)
        recordPrihod.Status = "OK"
        recordPrihod.save()
        return HttpResponseRedirect(reverse("Pospravljanje"))

    except:
        return HttpResponseRedirect(reverse("Pospravljanje"))


def ResetCiscenje(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.Status = ""
    record.ok1= None
    record.ok2= None
    record.ok3= None
    record.ok4= None
    record.cas_ciscenja= None
    record.save()

    # Če ima ta soba tudi prihod, moraš spremeniti status v "" za to sobo tudi v PospravljanjePrihodi
    StSobe = record.Soba
    try:
        recordPrihod = PospravljanjePrihodi.objects.get(Soba=StSobe)
        recordPrihod.Status = ""
        recordPrihod.save()
        return HttpResponseRedirect(reverse("Pospravljanje"))
    except:
        return HttpResponseRedirect(reverse("Pospravljanje"))


def vprasaj_kontrola_pospr(request, id):
    record = Pospravljanje.objects.get(id=id)
    context = {"soba": record}
    template= loader.get_template("form_vprasaj_kotr_pospr.html")    

    return HttpResponse(template.render(context, request))


def KontrolaPotrdi(request, id):
    record = Pospravljanje.objects.get(id=id)
    #record.cas_ciscenja = datetime.now()
    record.Status = "KO"
    record.save()

    StSobe = record.Soba
    try:
        recordPrihod = PospravljanjePrihodi.objects.get(Soba=StSobe)
        recordPrihod.Status = "KO"
        recordPrihod.save()
        return HttpResponseRedirect(reverse("Pospravljanje"))

    except:
        return HttpResponseRedirect(reverse("Pospravljanje"))


#    return HttpResponseRedirect(reverse("Pospravljanje"))


def KontrolaPonovi(request, id):  # POSPRAVLJANJE
    record = Pospravljanje.objects.get(id=id)
    record.Status = "PONOVI ČIŠČENJE"
    record.save()
    StSobe = record.Soba
    try:
        recordPrihod = PospravljanjePrihodi.objects.get(Soba=StSobe)
        recordPrihod.Status = "PONOVI ČIŠČENJE"
        recordPrihod.save()
        return HttpResponseRedirect(reverse("Pospravljanje"))

    except:
        return HttpResponseRedirect(reverse("Pospravljanje"))


#    return HttpResponseRedirect(reverse("Pospravljanje"))


def KontrolaReset(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.Status = ""
    record.cas_ciscenja=None
    record.ok1 = ""
    record.ok2 = ""
    record.ok3 = ""
    record.ok4 = ""
    record.save()

    StSobe = record.Soba
    try:
        recordPrihod = PospravljanjePrihodi.objects.get(Soba=StSobe)
        recordPrihod.Status = ""
        recordPrihod.save()
        return HttpResponseRedirect(reverse("Pospravljanje"))

    except:
        return HttpResponseRedirect(reverse("Pospravljanje"))
        
    
   


# PRIHODI
def PosprPrihodi(request):
    ObDatum = ObravnavaniDatum.objects.filter(Naziv="Ime").first()
    #ObDatum = ObravnavaniDatum.objects.get(id=1)

    Sobe = PospravljanjePrihodi.objects.all().values()
    StSob = (PospravljanjePrihodi.objects.all().count() -
             PospravljanjePrihodi.objects.filter(Status="OK").count() -
             PospravljanjePrihodi.objects.filter(Status="KO").count())
    template = loader.get_template("pospr_prihodi.html")
    context = {"SobeSeznam": Sobe, 
                "STSOB": StSob, 
                "ObDatum": ObDatum, 
                "DvoPosteljneSobe": L_2posteljneSobe,
                "StiriPosteljneSobe": L_4posteljneSobe,
                }
    
    # Pošlji email, da so vsi PRIHODI POSPRAVLJENI
    # JSON
   
    JS_file = os.path.join(settings.BASE_DIR, 'Aplikacija//static//json//jsonFILE_Prihodi.json')
    
    if StSob == 0:
        with open(JS_file, "r", encoding="utf-8") as f:
            json_file = json.load(f)
        if "VseSobeOK" in json_file:
            pass
        else:
            send_mail(subject="Vsi PRIHODI OK ", 
                message="PRIHODI ZAKLJUČENI", from_email=settings.EMAIL_HOST_USER, recipient_list=[settings.RECIPIENT_ADDRESS,]
                    )
        
            # v Json shrani list z informacijo, da so vse sobe OK
            with open(JS_file, "w", encoding="utf-8") as f:
                    json.dump(["VseSobeOK"], f, ensure_ascii=False, indent=4)
        
    else:
        # v Json shrani list z informacijo, da vse sobe ni OK
        with open(JS_file, "w", encoding="utf-8") as f:
                json.dump(["VseSobeNIOK"], f, ensure_ascii=False, indent=4)
    
    
    
    
    return HttpResponse(template.render(context, request))


def PotrdiCiscenjePrh(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = "OK"
    record.save()
    return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    # StSobe = record.Soba
    # try:
    #     recordPospravljanje = Pospravljanje.objects.get(Soba=StSobe)
    #     recordPospravljanje.Status = "OK"
    #     recordPospravljanje.save()
    #     return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    # except:
    #     return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))


def ResetCiscenjePrh(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = ""
    record.save()
    return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

    # StSobe = record.Soba
    # try:
    #     recordPospravljanje = Pospravljanje.objects.get(Soba=StSobe)
    #     recordPospravljanje.Status = ""
    #     recordPospravljanje.save()
    #     return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    # except:
    #     return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))


# PRIHODI - KONTROLA
def KontrolaPrihodiPotrdi(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = "KO"
    record.save()
    #return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    
    StSobe = record.Soba
    try:
        recordPrihod = Pospravljanje.objects.get(Soba=StSobe)
        recordPrihod.Status = "KO"
        recordPrihod.save()
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

    except:
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))


def KontrolaPrihodiPonovi(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = "PONOVI ČIŠČENJE"
    record.save()
    return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

    # StSobe = record.Soba
    # try:
    #     recordPrihod = Pospravljanje.objects.get(Soba=StSobe)
    #     recordPrihod.Status = "PONOVI ČIŠČENJE"
    #     recordPrihod.save()
    #     return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

    # except:
    #     return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

def KontrolaPrihodiReset(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = ""
    record.save()
    StSobe = record.Soba
    try:
        recordPrihod = Pospravljanje.objects.get(Soba=StSobe)
        recordPrihod.Status = ""
        recordPrihod.ok1= None
        recordPrihod.ok2= None
        recordPrihod.ok3= None
        recordPrihod.ok4= None
        recordPrihod.cas_ciscenja= None
        recordPrihod.save()
        
        
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

    except:
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    
    
    






def DetajliEmail(request, id):
    soba= Pospravljanje.objects.get(id=id)
    message= request.POST['sporocilo']
    send_mail(subject=("Soba "+ str(soba.Soba) + ": " + message), 
    message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[settings.RECIPIENT_ADDRESS,]
    )
    return HttpResponseRedirect(reverse('Pospravljanje'))

def DetajliPrhEmail(request, id):
    soba= PospravljanjePrihodi.objects.get(id=id)
    message=request.POST['sporocilo']
    send_mail(subject=("Soba "+ str(soba.Soba) +": " + message), 
    message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[settings.RECIPIENT_ADDRESS,]
    )
    return HttpResponseRedirect(reverse('Pospravljanje_Prihodi'))








def Detajli(request, id):
    #SSoba = Pospravljanje.objects.get(id=id)
    #SobaDetajl = SSoba.Soba
    #SobaDetajl = PodatkiGosti.objects.get(StSobe = SobaDetajl)
    SobaDetajl = Pospravljanje.objects.get(id=id)
    template = loader.get_template("detajli.html")
    context = {"SobaDetajl": SobaDetajl}
    return HttpResponse(template.render(context, request))


# OSTALE KOMANDE - iz detaljov.html
def GostiSliVen(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.Status = "ŠLI VEN"
    record.save()
    StSobe = record.Soba
    try:
        recordPospravljanjePrh = PospravljanjePrihodi.objects.get(Soba=StSobe)
        recordPospravljanjePrh.Status = "ŠLI VEN"
        recordPospravljanjePrh.save()
        return HttpResponseRedirect(reverse("Pospravljanje"))
    except:
        return HttpResponseRedirect(reverse("Pospravljanje"))

    #return HttpResponseRedirect(reverse("Pospravljanje"))


def vpras_pred_potrd_sli_ven(request, id):
    record = Pospravljanje.objects.get(id=id)
    context = {"soba": record}
    template = loader.get_template("form_vprasaj_zajtrk.html")
    return HttpResponse(template.render(context, request))






def GostiSliVenZajtrk(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.Status = "ŠLI VEN"
    record.save()
    StSobe = record.Soba
    try:
        recordPospravljanjePrh = PospravljanjePrihodi.objects.get(Soba=StSobe)
        recordPospravljanjePrh.Status = "ŠLI VEN"
        recordPospravljanjePrh.save()
        return HttpResponseRedirect(reverse("zajtrk"))
    except:
        return HttpResponseRedirect(reverse("zajtrk"))


def GostiSliVenZajtrkReset(request, id):
    record= Pospravljanje.objects.get(id=id)
    record.Status = ""
    record.save()
    return HttpResponseRedirect(reverse("zajtrk"))




def GostiSliVenPrihodi(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = "ŠLI VEN"
    record.save()
    StSobe = record.Soba
    try:
        recordPospravljanjePrh = Pospravljanje.objects.get(Soba=StSobe)
        recordPospravljanjePrh.Status = "ŠLI VEN"
        recordPospravljanjePrh.save()
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    except:
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))



def GostiNocejoCiscenja(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.Status = "NE CISTI!"
    record.save()
    return HttpResponseRedirect(reverse("Pospravljanje"))


def popravi_akcija_na_pospravi(request, id):
    Pospravljanje.objects.filter(id=id).update(Akcija="pospravi")
    return HttpResponseRedirect(reverse("Pospravljanje"))
    
def popravi_akcija_na_odhod(request, id):
    Pospravljanje.objects.filter(id=id).update(Akcija="odhod")
    return HttpResponseRedirect(reverse("Pospravljanje"))

def popravi_akcija_na_menjava(request, id):
    Pospravljanje.objects.filter(id=id).update(Akcija="menjava")
    return HttpResponseRedirect(reverse("Pospravljanje"))







def DetaljiPrihod(request, id):
    SobaDetajl = PospravljanjePrihodi.objects.get(id=id)
    template = loader.get_template("detajliPrihod.html")
    context = {"SobaDetajl": SobaDetajl}
    return HttpResponse(template.render(context, request))


def Zajtrk(request):
    ObDatum = ObravnavaniDatum.objects.filter(Naziv="Ime").first()
    
    ob_datum_dt = datetime.strptime(ObDatum.DatumObravnavani, "%d.%m.%Y") - timedelta(days=1)
    dan = ob_datum_dt.day
    if dan < 10:
        dan = "0" + str(dan)
    mesec = ob_datum_dt.month
    if mesec < 10:
        mesec = "0" + str(mesec)
    ob_datum_ddmm = str(dan) + "." + str(mesec) + "."
    
    sobe = Pospravljanje.objects.all().values().order_by("status_zajtrk_num")        #"StatusZajtrk")
    
    # Koliko sob mora še priti?
    stZajtrkov = sobe.count(
    ) - sobe.filter(StatusZajtrk="OK").count()

    # Koliko oseb mora še priti na zajtrk?
    st_oseb = sobe.exclude(StatusZajtrk="OK")
    se_oseb = 0
    for x in st_oseb:
        se_oseb= se_oseb + int(x["Oseb"])
    
    

    # Iskanje zadnje očiščene sobe:
    zadnja_ociscena_soba = sobe.order_by("-cas_ciscenja").first()
    st_sobe_zadnje_ocisc = zadnja_ociscena_soba["Soba"]
    # Na začetku še nobena soba ne bo očiščena, zato ne smo biti nobena označena - variabli dam vrednost št sobe= 0:
    if zadnja_ociscena_soba["cas_ciscenja"] == None:
        st_sobe_zadnje_ocisc = 0
    
    # Iskanje zadnjega zajtrka:
    zadnji_zajtrk_soba = sobe.order_by("-cas_zajtrka").first()
    zadnji_zajtrk_soba = zadnji_zajtrk_soba["Soba"]

    list_nov_prh = []
    #for soba in sobe:
     #   if soba.od

    template = loader.get_template("zajtrk.html")
    context = {
        "SobeSeznam": sobe,
        "ObDatum": ObDatum,
        "StZajtrk": stZajtrkov,
        "ob_datum_ddmm": ob_datum_ddmm,
        "st_sobe_zadnje_ocisc": st_sobe_zadnje_ocisc,
        "se_oseb": se_oseb,
        "st_sobe_zadnji_zajtrk": zadnji_zajtrk_soba
    }

    return HttpResponse(template.render(context, request))

def vprasaj_zajtrk_ok_1_2(request, id):
    record = Pospravljanje.objects.get(id=id)
    template = loader.get_template("form_vprasaj_zajtrk_ok_1_2.html")
    context = {"soba": record}

    return HttpResponse(template.render(context, request))


def PotrdiZajtrk(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.StatusZajtrk = "OK"
    record.cas_zajtrka = datetime.now()
    record.save()
    return HttpResponseRedirect(reverse("zajtrk"))


def ResetZajtrk(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.StatusZajtrk = ""
    record.cas_zajtrka = None
    record.save()
    return HttpResponseRedirect(reverse("zajtrk"))


def PotrdiZajtrkPOL(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.StatusZajtrk = "1/2"
    record.save()
    return HttpResponseRedirect(reverse("zajtrk"))


def GrafZasedenost(request):
    Sobe = Graf.objects.all().values()
    Template = loader.get_template("graf.html")
    Context = {"Sobe": Sobe,
                }
    return HttpResponse(Template.render(Context, request))

def GrafFooter(request):
    Sobe = Graf.objects.all()
    Template = loader.get_template("graf_footer.html")
    Context = {"Sobe": Sobe,
                }
    return HttpResponse(Template.render(Context, request))

def PrazneSOBE(request):
    ObDatum = ObravnavaniDatum.objects.get(Naziv="Ime")
    Sobe = PrazneSobe.objects.all().values()
    Template = loader.get_template("prazneSobe.html")
    Context = {"Sobe": Sobe, "ObDatum": ObDatum}
    return HttpResponse(Template.render(Context, request))



def CheckLIST(request, str):
    tekst = (str)
    
    id=int(tekst.split(sep="_")[0])   #  ('2565','Pospravljanje)
    vrstaDela = (tekst.split(sep="_")[1]) # ali je pospravljanje ali prihodi

    # Številka sobe, za tekst na vrhu tabele: Checklista za sobo 44
    if vrstaDela =="pospravljanje":
        Record = Pospravljanje.objects.get(id=id)
    elif vrstaDela =="prihodi":
        Record = PospravljanjePrihodi.objects.get(id=id)
    
    
    StSobe = Record.Soba
    # V db dodaj ID sobe v SQL, da se lahko po potrditvi vrneš na ChList formular
    IdSobe = ChListSobaID.objects.get(Opis = "SobaID")
    if vrstaDela =="pospravljanje":
        IdSobe.SobaID = f'{id}_pospravljanje'
    elif vrstaDela =="prihodi":
        IdSobe.SobaID = f'{id}_prihodi'
    

    # V vsakem pospr.prihodi imaš še polja "ok1" ok2... ok4, ki jih 
    # narediš QS za record z id-jem
    Akcija = Pospravljanje.objects.filter(Soba=StSobe).values("Status","ok1","ok2","ok3","ok4").first()
    IdSobe.StSobe = StSobe
    IdSobe.save()
    # Prenesi v template vse elemente formularja
    #Akcija = CheckLista.objects.all().values()
    template = loader.get_template("checklist.html")
    context = {"Akcija": Akcija,
                "Soba": StSobe,
                 }

    # ugotovi, ali so vsi elementi OK, če da, se vrni na pospravljanje
    
    if (Akcija["ok1"] == "OK" and Akcija["ok2"] == "OK" and Akcija["ok3"] == "OK" and Akcija["ok4"] == "OK"): 
        # print("TTTTTTT")
        IdSobe.VseOK = "VseOK"
        IdSobe.save()
        # V sobi , ki je imala vse OK, popravi status v OK. To naredi v tabeli pospravljanje in pospravljenjePrihodi
        if vrstaDela =="pospravljanje":
            SobaZvseOK = Pospravljanje.objects.get(Soba=StSobe)
            SobaZvseOK.Status="OK"
            SobaZvseOK.cas_ciscenja = datetime.now()
            SobaZvseOK.save()
        elif vrstaDela =="prihodi":
            SobaZvseOK = PospravljanjePrihodi.objects.get(Soba=StSobe)
            SobaZvseOK.Status="OK"
            SobaZvseOK.save()
            #prihodi-_ Lahko da ta soba ni v prihodih,
        try:
            if vrstaDela =="pospravljanje":
                SobaZvseOK = PospravljanjePrihodi.objects.get(Soba=StSobe)
            elif vrstaDela =="prihodi":
                SobaZvseOK = Pospravljanje.objects.get(Soba=StSobe)
            
            SobaZvseOK.Status="OK"
            SobaZvseOK.save()
            if vrstaDela =="pospravljanje":
                return HttpResponseRedirect("/pospravljanje/")
            elif vrstaDela =="prihodi":
                return HttpResponseRedirect("/pospravljanje_prihodi/")
        except:
            if vrstaDela =="pospravljanje":
                return HttpResponseRedirect("/pospravljanje/")
            elif vrstaDela =="prihodi":
                return HttpResponseRedirect("/pospravljanje_prihodi/")
    
    else:
    
        return HttpResponse(template.render(context, request))




def CheckLISTconfirm(request, str):
    SobaID = ChListSobaID.objects.get(Opis ="SobaID") # To je "nerodna" pomoč, da sem sploh sranil ID sobe v sql
    StSobe = SobaID.StSobe
    SobaID = SobaID.SobaID
    record = Pospravljanje.objects.get(Soba = StSobe)
    
    if str == "ok1":
        record.ok1 = "OK"
    elif str == "ok2":
        record.ok2 = "OK"
    elif str == "ok3":
        record.ok3 = "OK"
    elif str == "ok4":
        record.ok4 = "OK"

    #record.Status="OK"
    record.save()
    httpText=(f"/checklist/{SobaID}")
    return HttpResponseRedirect(httpText)


def Recepcija(request):
    template = loader.get_template("recepcija.html")
    
    if request.method == "POST":
        if "reset_zadnji" in request.POST:
            print("reset")
            # Iz statusa check in za zadnjo sobo odstrani OK
            zadnja_soba_cin = PospravljanjePrihodi.objects.order_by("-cas_checkin").first()
            zadnja_soba_cin.StatusCheckIn = ""
            zadnja_soba_cin.cas_checkin = None
            zadnja_soba_cin.save()
        sobe = PospravljanjePrihodi.objects.exclude(StatusCheckIn="OK")  #all().values()
    else: # GET
    
        sobe = PospravljanjePrihodi.objects.exclude(StatusCheckIn="OK")  #all().values()
    st_se_cin = PospravljanjePrihodi.objects.exclude(StatusCheckIn="OK").count()  #all().values()
    context={"Sobe":sobe, "st_se_cin": st_se_cin}
    return HttpResponse(template.render(context,request))

def RecepcijaDetajli(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    template = loader.get_template("recepcija_detajli.html")
    context = {"SobaDetajl":record}
    return HttpResponse(template.render(context, request))

def RecepcijaCheckInOK(request, id):
    record= PospravljanjePrihodi.objects.get(id=id)
    record.StatusCheckIn="OK"
    record.cas_checkin = datetime.now()
    record.save()
    return HttpResponseRedirect("/recepcija")    
    
  

def recep(request):
    template = loader.get_template("recep.html")
    context = {}
    return HttpResponse(template.render(context, request))



#TEST TEST TEST Create your views here.
"""def home_view(request):
    context ={}
    context['forma']= InputForm()
    return render(request, "formularTEST.html", context)"""




# def form_home(request):
#     gosti = VnosGostov.objects.all().values()
#     template = loader.get_template("form_home.html")
#     context = {"gost":gosti}
#     return HttpResponse(template.render(context, request))



# def form_vnos(request):
#     submitted = False # Dokler ni gumb, form ni submt (Codemy.com)
#     if request.method == "POST":
#         formular = VnosRezForm(request.POST)
#         #formular = VnosRezForm(data={"imestranke":"Peter","agencija":"Nasi"})
#         if formular.is_valid():
#             formular.save()
#             return HttpResponseRedirect("/form_vnos?submitted=True")
            
#     else:  # GET __Form še ni bil (pravilno) izpolnjen
#         formular = VnosRezForm
#         if "submitted" in request.GET:  # Ali je bil form že submitan?
#             submitted = True


    
#     context ={"forma": formular, "submitted":submitted, "testImeStranke":"Jože Novak"}
    
#     return render(request, "form_vnos.html", context)
    

# def form_update(request, id):
#     record = VnosGostov.objects.get(id=id)
#     idGosta = id
#     form = UpdateRezForm(instance=record)           #VnosRezForm(instance=record)
#     context= {"forma": form, "IdGosta":idGosta}
#     template = loader.get_template("form_update.html")
#     return HttpResponse(template.render(context, request))


# def form_updated(request, id):
    
#     gost = VnosGostov.objects.get(id=id)
#     template=("form_home.html")
#     if request.method == 'POST':
#         form = VnosRezForm(request.POST, instance=gost)
#         if form.is_valid():
#             # update the existing `Band` in the database
#             form.save()
#             # redirect to the detail page of the `Band` we just updated
#             #return HttpResponseRedirect(template, gost.id)
#             return HttpResponseRedirect("/form_home")
#     #else:
#     #    form = VnosRezForm(instance=gost)

#     #return HttpResponse(template.render(request,{'form': form}))



# # FORM DJANGO TUTOR
# from .forms import NameForm

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     submitted = False
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect("/form_vnos?submitted=True")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#         print("NATISNI:" + str(request.GET))
#         if "submitted" in request.GET:  # Ali je bil form že submitan?
#             submitted = True

#     return render(request, 'form_vnos.html', {'forma': form, "submitted": submitted})