from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from django.urls import reverse

import json
import os
from django.conf import settings

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime, time, timedelta, timezone

from .definicije.form_graf import *
from .definicije.iskanjeProstihSob import *
from .definicije.tabelaProsteSobe import *

import environ
environ.Env.read_env()
env = environ.Env()

# Create your views here.

L_2posteljneSobe = [10,11,12,20,21,30,31,32,34,35,36,37,38,39,43,45,50,51]
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
    current_user = request.user
    print(current_user)
    if current_user.groups.filter(name='boss').exists():   # Imaš 2 groups: worker, boss
        print("OK")
    groups = request.user.groups.all()
    
    # CHECKLISTA ####
    # Izbriši vse OK v tabeli Checklista
    CheckLista.objects.all().update(Status="")
    
    ##################
    
    ObDatum = ObravnavaniDatum.objects.filter(Naziv="Ime").first()
    #ObDatum = ObravnavaniDatum.objects.get(id=1)
    sobe = Pospravljanje.objects.all().values()
    StSob = (Pospravljanje.objects.all().count() -
             Pospravljanje.objects.filter(Status="OK").count() -
             Pospravljanje.objects.filter(Status="KO").count())
    # Ugotovi, koliko sobPrihodi je potrebno še pregledati - ta podatek
    prihodi = PospravljanjePrihodi.objects.filter(Status="OK").count()
    stVsehSobPrih = PospravljanjePrihodi.objects.all().count()
    seSobPrihZaPreveriti = stVsehSobPrih - prihodi - PospravljanjePrihodi.objects.filter(
        Status="KO").count()
    template = loader.get_template("pospravljanje.html")
    context = {
        "groups": groups,
        "SobeSeznam": sobe,
        "STSOB": StSob,
        "ObDatum": ObDatum,
        "SeSobPrih": seSobPrihZaPreveriti,
        "DvoPosteljneSobe": L_2posteljneSobe,   # List je na vrhu tega file
        "StiriPosteljneSobe": L_4posteljneSobe,
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


def PotrdiCiscenje(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.Status = "OK"
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


def KontrolaPotrdi(request, id):
    record = Pospravljanje.objects.get(id=id)
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


def KontrolaPonovi(request, id):
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
    StSobe=record.Soba
    record.Status = ""
    record.save()
    try:
        recordPrihod = PospravljanjePrihodi.objects.get(Soba = StSobe)
        recordPrihod.ok1 = ""
        recordPrihod.ok2 = ""
        recordPrihod.ok3 = ""
        recordPrihod.ok4 = ""
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
                message="PRIHODI ZAKLJUČENI", from_email="gasperin.hotel@gmail.com", recipient_list=["peter.gasperin@siol.net",]
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

    StSobe = record.Soba
    try:
        recordPospravljanje = Pospravljanje.objects.get(Soba=StSobe)
        recordPospravljanje.Status = "OK"
        recordPospravljanje.save()
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    except:
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))


def ResetCiscenjePrh(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = ""
    record.save()

    StSobe = record.Soba
    try:
        recordPospravljanje = Pospravljanje.objects.get(Soba=StSobe)
        recordPospravljanje.Status = ""
        recordPospravljanje.save()
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
    except:
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))


# PRIHODI - KONTROLA
def KontrolaPrihodiPotrdi(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = "KO"
    record.save()

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
    StSobe = record.Soba
    try:
        recordPrihod = Pospravljanje.objects.get(Soba=StSobe)
        recordPrihod.Status = "PONOVI ČIŠČENJE"
        recordPrihod.save()
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

    except:
        return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))

def KontrolaPrihodiReset(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    record.Status = ""
    record.ok1 = ""
    record.ok2 = ""
    record.ok3 = ""
    record.ok4 = ""
    record.save()
    return HttpResponseRedirect(reverse("Pospravljanje_Prihodi"))
#"gasperin.hotel@gmail.com"
def DetajliEmail(request, id):
    soba= Pospravljanje.objects.get(id=id)
    message= request.POST['sporocilo']
    send_mail(subject=("Soba "+ str(soba.Soba) + ": " + message), 
    message=message, from_email="gasperin.hotel@gmail.com" , recipient_list=["peter.gasperin@siol.net",]
    )
    return HttpResponseRedirect(reverse('Pospravljanje'))

def DetajliPrhEmail(request, id):
    soba= PospravljanjePrihodi.objects.get(id=id)
    message=request.POST['sporocilo']
    send_mail(subject=("Soba "+ str(soba.Soba) +": " + message), 
    message=message, from_email="gasperin.hotel@gmail.com", recipient_list=["peter.gasperin@siol.net",]
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
    record.Status = "NE ČISTI!"
    record.save()
    return HttpResponseRedirect(reverse("Pospravljanje"))


def DetaljiPrihod(request, id):
    SobaDetajl = PospravljanjePrihodi.objects.get(id=id)
    template = loader.get_template("detajliPrihod.html")
    context = {"SobaDetajl": SobaDetajl}
    return HttpResponse(template.render(context, request))


def Zajtrk(request):
    ObDatum = ObravnavaniDatum.objects.filter(Naziv="Ime").first()
    stZajtrkov = Pospravljanje.objects.all().count(
    ) - Pospravljanje.objects.filter(StatusZajtrk="OK").count()
    sobe = Pospravljanje.objects.all().values()
    template = loader.get_template("zajtrk.html")
    context = {
        "SobeSeznam": sobe,
        "ObDatum": ObDatum,
        "StZajtrk": stZajtrkov,
    }

    return HttpResponse(template.render(context, request))


def PotrdiZajtrk(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.StatusZajtrk = "OK"
    record.save()
    return HttpResponseRedirect(reverse("zajtrk"))


def ResetZajtrk(request, id):
    record = Pospravljanje.objects.get(id=id)
    record.StatusZajtrk = ""
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
    sobe = PospravljanjePrihodi.objects.all().values()
    context={"Sobe":sobe}

    return HttpResponse(template.render(context,request))

def RecepcijaDetajli(request, id):
    record = PospravljanjePrihodi.objects.get(id=id)
    template = loader.get_template("recepcija_detajli.html")
    context = {"SobaDetajl":record}
    return HttpResponse(template.render(context, request))

def RecepcijaCheckInOK(request, id):
    record= PospravljanjePrihodi.objects.get(id=id)
    record.StatusCheckIn="OK"
    record.save()
    return HttpResponseRedirect("/recepcija")    
    
  


#TEST TEST TEST Create your views here.


"""def home_view(request):
    context ={}
    context['forma']= InputForm()
    return render(request, "formularTEST.html", context)




def form_home(request):
    gosti_seznam = VnosGostov.objects.all().order_by("-id").values()
    template = loader.get_template("form_home.html")
    
    page = request.GET.get('page', 1)
 
    paginator = Paginator(gosti_seznam, 200)
    try:
        gosti = paginator.page(page)
    except PageNotAnInteger:
        gosti = paginator.page(1)
    except EmptyPage:
        gosti = paginator.page(paginator.num_pages)
 
    
    context = {"gost":gosti}
    return HttpResponse(template.render(context, request))


def form_Avtovnos(request):
    # Pridobi podatke o rez
    cena, ime, agencija, stOseb, datumOD, datumDO, RNA = Autofill_def()
    
    submitted = False # Dokler ni gumb, form ni submt (Codemy.com)
    if request.method == "POST":
        formular = VnosRezForm(request.POST)
        #formular = VnosRezForm(data={"imestranke":"Peter","agencija":"Nasi"})
        if formular.is_valid():
            formular.save()
            formular=VnosRezForm()
            
            return HttpResponseRedirect("/form_Avtovnos?submitted=True")
        else:
            print("Formular ni v celoti izpolnjen. Ni valid")
            
    else:  # GET __Form še ni bil (pravilno) izpolnjen
        formular = VnosRezForm(data={"CENA":cena, "imestranke": ime, "agencija":agencija, "SO":stOseb, "od":datumOD,
    "do": datumDO, "RNA":RNA})
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True


    
    context ={"forma": formular, "submitted":submitted, }
    #"ImeStranke":"Jože Novak", "Agencija":agencija, "StOseb":stOseb, "DatumOD":datumOD,
    #"DatumDO": datumDO}
    
    return render(request, "form_Avtovnos.html", context)


def form_vnos_rocni(request):
    
    submitted = False # Dokler ni gumb, form ni submt (Codemy.com)
    # Pridobi podatke od JSONA
    JS_file = os.path.join(settings.BASE_DIR, 'Aplikacija//static//json//jsonFILE_IzborSob.json')
    with open(JS_file, "r", encoding="utf-8") as f:
        jsonData = json.load(f)
    
    if jsonData[0]!="0":
        od = jsonData[1]
        do = jsonData[2]
        tip = jsonData[3]
    else:
        print("Ni podatkov")
    
    
    if request.method == "POST":
        formular = VnosRezForm(request.POST)
        #formular = VnosRezForm(data={"imestranke":"Peter","agencija":"Nasi"})
        if formular.is_valid():
            formular.save()
            formular=VnosRezForm()
            
            return HttpResponseRedirect("/form_vnos_rocni?submitted=True")
        else:
            print("Formular ni v celoti izpolnjen. Ni valid")
            
    else:  # GET __Form še ni bil (pravilno) izpolnjen
        if jsonData[0]!="0":
            formular = VnosRezForm(data={"od": od, "do": do, "tip": tip})
        #else:
        #formular = VnosRezForm()
        
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True

    
    context ={"forma": formular, "submitted":submitted,}
    
    return render(request, "form_vnos_rocni.html", context)


def form_vnos_izbor_sob(request):
    submitted = False # Dokler ni gumb, form ni submt (Codemy.com)
    if request.method == "POST":
        formular = izborProsteSobe(request.POST)
        #formular = VnosRezForm(data={"imestranke":"Peter","agencija":"Nasi"})
        if formular.is_valid():
            datumOD = formular.cleaned_data['od'] 
            
            datumDO = formular.cleaned_data['do']
            
            
            tipS = formular.cleaned_data['tip']
            
            L_prosteSobe = proste_sobe(tipS, datumOD, datumDO)
            L_prosteSobeJson = proste_sobe(tipS, datumOD, datumDO)
            datumOD = datumOD.strftime("%d.%m.%Y")  
            datumDO = datumDO.strftime("%d.%m.%Y")  
            
            # Izdelaj tabelo s prostimi sobami
            Datum_OD= pd.to_datetime(datumOD, format=("%d.%m.%Y"))
            Datum_DO= pd.to_datetime(datumDO, format=("%d.%m.%Y"))
            #print(type(DatumOD), DatumOD)
        
            data=IzdelavaGrafa(Datum_OD,"DN")
            
            tabelaProstihSob(data, Datum_OD, Datum_DO, L_prosteSobe)
            print(tabelaProstihSob)
            
            # Vnos podatkov v JSON #######
            podatki=[
                L_prosteSobeJson,
                datumOD,
                datumDO,
                tipS,
            ]

            JS_file = os.path.join(settings.BASE_DIR, 'Aplikacija//static//json//jsonFILE_IzborSob.json')
            with open(JS_file, "w", encoding="utf-8") as f:
                            json.dump(podatki, f, ensure_ascii=False, indent=4)
            
            ##############  END json ########
            
            return HttpResponseRedirect("/form_vnos_izbor_sob/form_izberiSobo")            #"/form_vnos_rocni")
        else:
            print("Formular ni v celoti izpolnjen. Ni valid")
            
    else:  # GET __Form še ni bil (pravilno) izpolnjen
        formular = izborProsteSobe() #(data={"imestranke":"Peter","agencija":"Nasi"})
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True

    
    context ={"forma": formular, "submitted":submitted,
    }
    
    return render(request,"form_predVnos.html" , context)  # "form_vnos_rocni.html"



def form_izberi_sobo(request):
    JS_file = os.path.join(settings.BASE_DIR, 'Aplikacija//static//json//jsonFILE_IzborSob.json')
    with open(JS_file, "r", encoding="utf-8") as f:
        jsonData = json.load(f)
    
    listSob = jsonData[0]
    
   
    
    if request.method == "POST":
        formular = IzberiSobo(request.POST)
        if formular.is_valid():
            formular = IzberiSobo()
            
            
            return HttpResponseRedirect("/form_izberiSobo")
        else:
            print("Formular ni v celoti izpolnjen. Ni valid")
            
    else:  # GET __Form še ni bil (pravilno) izpolnjen
        #formular = IzberiSobo.fields['izberisobo'].choices = tuppleSob
        formular = IzberiSobo() #data={ 'izberisobo': tuppleSob })
        
   
  
    context ={"forma": formular, "choices": listSob }
    
    
    return render(request, "form_izberiSobo.html", context)

    



def form_updated(request, id):
    
    gost = VnosGostov.objects.get(id=id)
    template=loader.get_template("form_update.html")
    form = VnosRezForm(request.POST, instance=gost)
    
    if request.method == 'POST':
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            #return HttpResponseRedirect(template, gost.id)
            return HttpResponseRedirect("/form_home")
        else:
            print("Form ni VALID")
    else: #  GET
        form = VnosRezForm(instance=gost)
        

    return HttpResponse(template.render({"forma":form, "gost":gost}, request))


def delete_gost(request,id):
    gost = VnosGostov.objects.get(id=id)
    template=loader.get_template("form_delete.html")
    if request.method == "POST":
        gost.delete()
        return HttpResponseRedirect("/form_home")

    
    context={"item":gost}
    return HttpResponse(template.render(context, request))



def form_graf(request):
    # pridobi podatke iz arhiva rezervacij
    IzdelavaGrafa(pd.to_datetime("today"),"R_Optimi")  #"R_Optimi"))   "DN")) R_Optimi_iskanjeRez
    
    if request.method == "POST":
        formular = izborDatuma(request.POST)
        if formular.is_valid():
            datum = formular.cleaned_data['datum'] # cleaned_data da dobiš vrednost forma po submitu v views.py
            IzdelavaGrafa(pd.to_datetime(datum),"R_Optimi") 
            
    else:
        formular = izborDatuma()
    
    
    #rezervacije = Graf.objects.all().values()
    rezervacije = Graf.objects.values("S0","S1","S2","S3","S4","S5","S6","S7",
                    "S8","S9","S10","S11","S12","S13","S14","S15","S16","S17",
                    "S18","S19","S20","S21","S22","S23","S24","S25","S26","S27") 
    context= {"rezervacije":rezervacije, "formDatum": formular}
    template = loader.get_template("form_graf.html")

    return HttpResponse(template.render(context, request))

def updateIzGrafa(request, komande):
    
    
    id=int(komande.split(sep="_")[0])  
    
    
    gost = VnosGostov.objects.get(id=id)
    template=loader.get_template("form_update.html")
    form = VnosRezForm(request.POST, instance=gost)
    
    if request.method == 'POST':
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            #return HttpResponseRedirect(template, gost.id)
            return HttpResponseRedirect("/form_home")
        else:
            print("Form ni VALID")
    else: #  GET
        form = VnosRezForm(instance=gost)
        

    return HttpResponse(template.render({"forma":form, "gost":gost}, request))
    
    
    








def writetofile(request):
    f = open('C:/demo/test.txt', 'w')
    testfile = File(f)
    testfile.write('Welcome to this country')
    testfile.close
    f.close
    return HttpResponse()

def readfile(request):
    f = open("C:/Users/Hotel/Downloads/book.txt","r",encoding='utf8')
    if f.mode == 'r':
       contents =f.read()
       print (contents)
    return HttpResponse()   
"""