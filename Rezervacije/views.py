import clipboard # Shranjevanje v clipboard !!!!!!!!!!
import environ
environ.Env.read_env()
env = environ.Env()


from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import QueryDict

from django.urls import reverse

from django.db.models import Q, Count, Sum
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Aplikacija.models import Graf, Pospravljanje, PospravljanjePrihodi, PrazneSobe, ObravnavaniDatum


from .models import *
import json
import os
import pandas as pd

from datetime import datetime, timedelta, date
import datetime as dt

from .filters import RezervacijeFilter

from .forms import (VnosRezForm, izborDatuma, izborProsteSobeVnos, 
                    SearchForm, IzborAgencije, IzborDatumovPonudba, 
                    PonudbaForm, Bar_form, Dn_form_izberi_datum)
from .definicije.razno import *
from .definicije.autofill import *
from .definicije.graf import *
from .definicije.iskanjeProstihSob import *
from .definicije.tabelaProsteSobe import *
from .definicije.ponudbaIzdelava import *
from .definicije.ponudbaObdelava import *
from .definicije.dn_izracuni import *
from .definicije.app_podatki import *
from .definicije.info_tekst import *
from .definicije.grafikoni import *

from .definicije.dashboard import *
from .definicije.siteminder import *



"""def home_view(request):
    context ={}
    context['forma']= InputForm()
    return render(request, "formularTEST.html", context)"""



def form_rezervacije(request):
     # Get all VnosGostov objects
    if 'reset' in request.GET:
        return HttpResponseRedirect(request.path_info)
    
    queryset = VnosGostov.objects.filter(status_rez="rezervirano")

    # Create a FilterSet instance and apply the filter if the form is submitted
    filter_form = RezervacijeFilter(request.GET, queryset=queryset)
    filtered_queryset = filter_form.qs

    # Create a Paginator instance and get the current page number from the request's GET parameters
    paginator = Paginator(filtered_queryset, per_page=10)  # You can set the desired number of objects per page here
    page = request.GET.get('page', 1)

    # Get the Page object for the current page number
    page_obj = paginator.get_page(page)

    context = {
        'filter_form': filter_form,
        'page_obj': page_obj,
    }

    return render(request, 'form_rezervacije.html', context)









"""def form_rezervacije(request):
    gosti_seznam = VnosGostov.objects.filter(status_rez="rezervirano")
    # gosti_seznam = VnosGostov.objects.all().values()        #.order_by("-id").values()>> mi treba več -, ker je že definiran v models
    template = loader.get_template("form_rezervacije.html")
    search_form = SearchForm(request.GET)  # or None)
    if search_form.is_valid():
        query = search_form.cleaned_data.get("search_field")
        gosti_seznam = gosti_seznam.filter(
            imestranke__icontains=query).order_by('-id')[:20]

    page = request.GET.get('page', 1)

    paginator = Paginator(gosti_seznam, 10)
    try:
        gosti = paginator.page(page)
    except PageNotAnInteger:
        gosti = paginator.page(1)
    except EmptyPage:
        gosti = paginator.page(paginator.num_pages)

    context = {"gost": gosti, "form": search_form}
    return HttpResponse(template.render(context, request))

"""

def form_avtovnos_file(request):
    template = loader.get_template("form_predVnos_avto.html")
    context={}
    
    if request.method== "POST" and request.FILES:
        file = request.FILES["file"]
        vsebina = file.read()
        vsebina = vsebina.decode("utf-8")
        
        Autofill_def(tekst= vsebina)
        

        
        return HttpResponseRedirect("/form_avtovnos/")

    else: # GET
        return HttpResponse(template.render(context, request))


def avtovnos(request):
    
    
    JS_file = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    
    submitted = False  # Dokler ni gumb, form ni submt (Codemy.com)
    # Pridobi podatke o rez
    podatki = odpriJson(js_file=JS_file)
    datumOD = podatki["od"] 
    datumDO = podatki["do"] 
    tip = podatki["tip_avto"]
    ime = podatki["ime"] 
    
    if request.method == "POST":
        formular = izborProsteSobeVnos(request.POST)
        if formular.is_valid():
            tipS = formular.cleaned_data['tip']
    
            # queryset >> pandas
            queryset = VnosGostov.objects.filter(status_rez="rezervirano")
            data = list(queryset.values())
            df_data = pd.DataFrame.from_records(data=data)
            # queryset >> pandas
            queryset_sifrant = SifrantSob.objects.all()
            data = list(queryset_sifrant.values())
            df_sifrant_sob = pd.DataFrame.from_records(data=data)
            
            L_prosteSobe = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
            L_prosteSobe = [x for x in L_prosteSobe if x != 99]
            
            L_prosteSobeJson = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
            L_prosteSobeJson = [x for x in L_prosteSobeJson if x != 99]

            # Izdelaj tabelo s prostimi sobami
            Datum_OD = pd.to_datetime(datumOD, format=("%d.%m.%Y"))
            Datum_DO = pd.to_datetime(datumDO, format=("%d.%m.%Y"))
            # print(type(DatumOD), DatumOD)
            
            data = IzdelavaGrafa(df_data, Datum_OD, "DN")

            tabelaProstihSob(data, Datum_OD, Datum_DO, L_prosteSobe)

            # Vnos podatkov v JSON #######

            js_file = os.path.join(
                settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
            jsonData = odpriJson(js_file=js_file)
            
            jsonData["list_prostih_sob"] = L_prosteSobeJson
            jsonData["tip"] = tipS

            shraniJson(js_file=js_file, jsonData=jsonData)
            
            ##############  END json ########

            if L_prosteSobeJson == []:
                formular = izborProsteSobeVnos(data={"od": datumOD, "do": datumDO})
                template = loader.get_template("form_predVnos.html")
                context = {"forma": formular, "errmsg":"Ni prostih sob tega tipa", "ime":ime,}
                return HttpResponse(template.render(context, request))
                
            else:
                return HttpResponseRedirect("/form_predvnos_rez/form_izberiSobo")


        else:
            print("Formular ni v celoti izpolnjen. Ni valid")

    else:  # GET __Form še ni bil (pravilno) izpolnjen
        #datumOD, datumDO, ime = Autofill_def()
        formular = izborProsteSobeVnos(data={"od": datumOD, "do": datumDO, "tip":tip})
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True

    context = {"forma": formular, "submitted": submitted,
               "ime":ime,
               }

    # "form_vnos_rocni.html"
    return render(request, "form_predVnos.html", context)




def predvnos_rezerv(request):  
    """Začetek vnosa- izbereš od, do , tip sobe + submit """
    
    # Počisti Json
    js_file = os.path.join(
            settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    shraniJson(js_file=js_file, jsonData={})
    
    submitted = False  # Dokler ni gumb, form ni submt (Codemy.com)
    if request.method == "POST":
        # vnesi zadnjo rezervacijo v ročni_vnos
        if "btn_zadnja" in request.POST:
            # pridobi zadnjo rezervacijo 
            zadnja_rez = VnosGostov.objects.filter(status_rez="rezervirano").order_by("-id").first()
            
            jsonData = {}
            jsonData["vrsta"]= "zadnja_rezervacija"
            jsonData["od"] = zadnja_rez.od
            jsonData["do"] = zadnja_rez.do
            jsonData["agencija"] = zadnja_rez.agencija
            jsonData["ime"]= zadnja_rez.imestranke
            jsonData["email"]= zadnja_rez.email
            jsonData["rna"]= zadnja_rez.RNA
            jsonData["zahteve"]= zadnja_rez.zahteve
            jsonData["drzava"]= zadnja_rez.DR
            jsonData["stanjeTtax"]= zadnja_rez.StanjeTTAX
            jsonData["tip"]= None
            jsonData["tip_avto"]= None
            jsonData["stsobe"]= None
            jsonData["list_prostih_sob"]= []
            jsonData["datumvnosa"]= datetime.strftime(datetime.now().date(), "%d.%m.%Y")
            jsonData["multiroom"]= None
            shraniJson(js_file=js_file, jsonData=jsonData)
            return HttpResponseRedirect("/form_avtovnos/")
        
        else:
            formular = izborProsteSobeVnos(request.POST) # od, do , tip
            # formular = VnosRezForm(data={"imestranke":"Peter","agencija":"Nasi"})
            if formular.is_valid():
                datumOD = formular.cleaned_data['od']
                datumDO = formular.cleaned_data['do']
                tipS = formular.cleaned_data['tip']
                

                
                # queryset >> pandas
                queryset = VnosGostov.objects.filter(status_rez="rezervirano")
                data = list(queryset.values())
                df_data = pd.DataFrame.from_records(data=data)
                # queryset >> pandas
                queryset_sifrant = SifrantSob.objects.all()
                data = list(queryset_sifrant.values())
                df_sifrant_sob = pd.DataFrame.from_records(data=data)
                
                
                L_prosteSobe = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
                L_prosteSobe = [x for x in L_prosteSobe if x != 99]
                L_prosteSobeJson = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
                L_prosteSobeJson = [x for x in L_prosteSobeJson if x!=99]
                
                # Izdelaj tabelo s prostimi sobami
                Datum_OD = pd.to_datetime(datumOD, format=("%d.%m.%Y"))
                Datum_DO = pd.to_datetime(datumDO, format=("%d.%m.%Y"))
                
                data = IzdelavaGrafa(df_data, Datum_OD, "DN")

                tabelaProstihSob(data, Datum_OD, Datum_DO, L_prosteSobe)

                # Vnos podatkov v JSON #######

                js_file = os.path.join(
                    settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
                jsonData = odpriJson(js_file=js_file)
                jsonData["vrsta"]= "rocni_vnos"
                jsonData["list_prostih_sob"] = L_prosteSobeJson
                jsonData["od"] = datumOD
                jsonData["do"] = datumDO
                jsonData["tip"] = tipS
                jsonData["agencija"]= "Nasi"
                
                shraniJson(js_file=js_file, jsonData=jsonData)
                
                ##############  END json ########
            
                # if "NI PROSTIH SOB" in L_prosteSobeJson:
                if L_prosteSobeJson == []:
                    formular = izborProsteSobeVnos(data={"od": datumOD, "do": datumDO})
                    template = loader.get_template("form_predVnos.html")
                    context = {"forma": formular, "errmsg":"Ni prostih sob tega tipa"}
                    return HttpResponse(template.render(context, request))
                    #render(request, template, context)
                    #return HttpResponseRedirect("/form_predvnos_rez/")
                else:
                    return HttpResponseRedirect("/form_predvnos_rez/form_izberiSobo")
            
            
            else:
                print("Formular ni v celoti izpolnjen. Ni valid")

    else:  # GET __Form še ni bil (pravilno) izpolnjen
        # (data={"imestranke":"Peter","agencija":"Nasi"})
        formular = izborProsteSobeVnos()
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True

    context = {"forma": formular, "submitted": submitted,
               }

    # "form_vnos_rocni.html"
    return render(request, "form_predVnos.html", context)


 
def form_vnos_rocni(request):
    submitted = False  # Dokler ni gumb, form ni submt (Codemy.com)
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    jsonData = odpriJson(js_file=js_file)
    
    od = jsonData["od"]
    do = jsonData["do"]
    tip = jsonData["tip"]
    datumvnosa = pd.to_datetime("today").strftime(format="%d.%m.%Y")
    stsobe = jsonData["stsobe"]
    
    if jsonData["vrsta"] == "avtovnos": # in jsonData: # Podatki od AVTOVNOSA
        od = jsonData["od"]
        do = jsonData["do"]
        tip = jsonData["tip"]
        ime = jsonData["ime"]
        stoseb = jsonData["stoseb"]
        cena = jsonData["cena"]
        agencija = jsonData["agencija"]
        rna = jsonData["rna"]
        zahteve = jsonData["zahteve"]
        email = jsonData["email"]
        drzava= jsonData["drzava"]
        avans_eur= jsonData["avans_eur"]
        if jsonData["rok_placila_avansa"] == None:
            rok_placila_avansa = None
        else:
            rok_placila_avansa= datetime.strptime(jsonData["rok_placila_avansa"],"%d.%m.%Y")

        if agencija == "Siteminder" or agencija == "Cesta" or agencija == "Nasi":
            stanjeTtax = "Ttax JE VKLJ"
        elif agencija == "":
            stanjeTtax = ""
        else:
            stanjeTtax = "Ttax NI VKLJ"
    
    if jsonData["vrsta"]== "zadnja_rezervacija":
        stsobe= jsonData["stsobe"]
        od = jsonData["od"]
        do = jsonData["do"]
        agencija= jsonData["agencija"]
        ime = jsonData["ime"]
        email= jsonData["email"]
        rna = jsonData["rna"]
        drzava = jsonData["drzava"]
        stanjeTtax= jsonData["stanjeTtax"]
        zahteve= jsonData["zahteve"]
        datumvnosa = jsonData["datumvnosa"] 
        stsobe = jsonData["stsobe"]
        tip = jsonData["tip"]
        

    #print(request.POST)
    
    # POST ############
    if request.method == "POST":
        formular = VnosRezForm(request.POST)
        if (request.POST['dniPredr'] == ''):

            dniPredr = 0



        if formular.is_valid():
            stoseb= formular.cleaned_data["SO"]
            formular.save()
            # dodaj še število oseb v json
            jsonData["stoseb"]= stoseb
            shraniJson(js_file=js_file, jsonData=jsonData)
            
            formular = VnosRezForm()
            
            # Pošlji na APP, če je od rezervacije manjši od 7 dni.
                # Če je ura 2000, naredi prenos na APP za jutri, sicer pa za danes
            if (datetime.strptime(od, "%d.%m.%Y") - datetime.now()).days < 7:
                datum_sedaj = datetime.strftime(datetime.now().date(), "%d.%m.%Y")
                
                if datetime.now().time().hour < 10:
                    ob_datum =datetime.strptime(datum_sedaj, "%d.%m.%Y")  # datetime.now()
                else:
                    ob_datum = datetime.strptime(datum_sedaj, "%d.%m.%Y")+ timedelta(days=1)
               
                data_class = App_podatki(ob_datum= ob_datum, vir="app")
                data_class.PodatkiZaWebApplic()
                
              
            return HttpResponseRedirect("/form_vnos_update_availability")
            #return HttpResponseRedirect("/form_vnos_rocni?submitted=True")

    ####   GET  #######
    else:  # GET __Form še ni bil (pravilno) izpolnjen
        
        if jsonData["list_prostih_sob"] != "0": # V jsonu so samo prvič v GET podatki o sobi in rezervaciji, potem se zbrišejo
            #Msg_Manjka_Avans=""
            if jsonData["vrsta"]== "avtovnos": # Podatki od AVTOVNOSA
                formular = VnosRezForm(data={"datumvnosa": datumvnosa, "od": od, "do": do, "tip": tip, "stsobe": stsobe,
                                         "imestranke": ime, "CENA": cena, "agencija": agencija, "RNA": rna, 
                                         "zahteve": zahteve, "email": email, "StanjeTTAX": stanjeTtax,
                                         "SO":stoseb, "DR": drzava, "AvansEUR": avans_eur,
                                         "RokPlacilaAvansa": rok_placila_avansa})
            elif jsonData["vrsta"]== "zadnja_rezervacija":
                formular = VnosRezForm(data={"od": od, "do": do, "imestranke": ime,
                                             "agencija": agencija, "RNA": rna, "stsobe": "",
                                             "zahteve": zahteve, "email": email, 
                                             "StanjeTTAX": stanjeTtax,
                                             "DR": drzava, "datumvnosa": datumvnosa,
                                             "tip": tip, "stsobe":stsobe,
                                             })
            
            
            
            else: #ročni vnos
                formular = VnosRezForm(data={"datumvnosa": datumvnosa, "od": od, "do": do, "tip": tip, "stsobe": stsobe})
        
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True


    dict_zahteve = {"Izberi":"Izberi", "2 rooms!":"2 rooms!","3 rooms!":"3 rooms!","4 rooms!":"4 rooms!",
                    "Quiet!":"Quiet!","High floor!":"High floor!",
                    "Must that room!":"Must that room!","":"","Repeat":"Repeat",
                    "1 adult":"1 adult","2 adults":"2 adults","3 adults":"3 adults",
                    "4 adults":"4 adults","1 ad 1 ch":"1 ad 1 ch","2 ad 2 ch":"2 ad 2 ch",
                    "2 ad 1 ch":"2 ad 1 ch","3 ad 1 ch":"3 ad 1 ch","ACAP":"ACAP",
                    "at 11:00":"at 11:00","at 12:00":"at 12:00","at 13:00":"at 13:00",
                    "at 14:00":"at 14:00","at 15:00":"at 15:00","at 16:00":"at 16:00",
                    "at 17:00":"at 17:00","at 18:00":"at 18:00","at 19:00":"at 19:00",
                    "at 20:00":"at 20:00","at 21:00":"at 21:00","at 22:00 informed":"at 22:00 informed",}
    context = {"forma": formular, "submitted": submitted, 
               "dict_zahteve": dict_zahteve}

    return render(request, "form_vnos_rocni.html", context)



def form_izberi_sobo(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    jsonData = odpriJson(js_file=js_file)
    listRazpolozljSob = jsonData["list_prostih_sob"]
    datumOD= jsonData["od"]
    datumDO= jsonData["do"]
    st_nocitev = (datetime.strptime(datumDO, "%d.%m.%Y") - datetime.strptime(datumOD, "%d.%m.%Y")).days 
    stolpec_Sxx_do = f"S{str(st_nocitev + 16)}" # TO je stolpec v tabeli, kjer se pojavi vertik. rdeča črta , ki označuje do (konec rezervacije)
    tipSobe= jsonData["tip"]
    
    if request.method == "POST":
        # formular = IzberiSobo(request.POST)
        # if formular.is_valid():
        # formular.cleaned_data['izberisobo']
        IzbranaSoba = request.POST.get("izberisobo")
        # print(IzbranaSoba)
        jsonData["stsobe"] = IzbranaSoba

        shraniJson(js_file=js_file, jsonData=jsonData)
       
            # formular = IzberiSobo()

        return HttpResponseRedirect("/form_vnos_rocni")
        # else:
        #   print("Formular ni v celoti izpolnjen. Ni valid")

    else:  # GET
        template = loader.get_template("form_izberiSobo.html")
        # PODATKI ZA GRAF
        # Briši vse instance v database Graf
        Graf.objects.all().delete()
        # queryset >> pandas
        queryset = VnosGostov.objects.filter(status_rez="rezervirano")
        data = list(queryset.values())
        df_data = pd.DataFrame.from_records(data=data)
        df_graf= IzdelavaGrafa(df_data, pd.to_datetime(datumOD, format="%d.%m.%Y"), "R_Optimi")
        # Pretvori Padas >> Queryset
        my_dict = df_graf.to_dict(orient="records")
        my_instances = [Graf(**d) for d in my_dict]
        Graf.objects.bulk_create(my_instances)
        rezervacije = Graf.objects.values("S0", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                          "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")

        listSob = seznamSob(tipSobe)
        # Odstrani 99
        listSob= [x for x in listSob if x!= 99]
        context = {"choices": listRazpolozljSob, 
                   "rezervacije": rezervacije, "listSob": listSob,
                   "stolpec_Sxx_do": stolpec_Sxx_do}

    return HttpResponse(template.render(context, request))

def update_availability(request):
    js_file = os.path.join(
            settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    podatki = odpriJson(js_file=js_file)
    datum_od = podatki["od"]
    datum_od_dt = datetime.strptime(datum_od, "%d.%m.%Y")
    datum_od_sm = datetime.strftime(datum_od_dt, "%Y-%m-%d")
    agencija = podatki["agencija"]
    info_tekst="Info teksta ni potrebno pošiljati"
    email=""
    pokazi_textarea_infotext = False
    submitted = False
    if agencija =="Siteminder" or agencija =="Booking.com" or agencija =="Expedia":
        pokazi_textarea_infotext = True
        ime = podatki["ime"]
        drzava = podatki["drzava"]
        stoseb= podatki["stoseb"]
        tip = podatki["tip"]
        multiroom= podatki["multiroom"]
        email = podatki["email"]
        info_tekst = info_tekst_def(ime, agencija, drzava, stoseb, tip, multiroom)
    
    template=loader.get_template("form_vnos_update_availability.html")
    
    if request.method == "POST":
        if "btn_uredi_sm" in request.POST:
            url_sitem = f"https://app.siteminder.com/web/extranet/hoteliers/96/inventory#!?startDate={datum_od_sm}"
            context={"zazeni_siteminder": url_sitem, }  
            clipboard.copy(url_sitem)
        
        if "btn_brez_sm" in request.POST:
            return HttpResponseRedirect("/form_rezervacije")
        
        if "btn_poslji_info" in request.POST:
            tekst_iz_textarea_www = request.POST.get("info_po_rezervaciji")
            email_iz_wwww = request.POST.get("email_www")
            submitted = True
            pokazi_textarea_infotext = False

            # zamenjaj email z email_www
            if email == "":
                email = email_iz_wwww

            if email != "":
                email = EmailMessage(subject="Important message ", 
                                    body= tekst_iz_textarea_www, #info_tekst, 
                                    from_email= settings.EMAIL_HOST_USER, 
                                    to= ["peter.gasperin@siol.net"] #[email]
                        )
                # Set the HTML version of the message
                email.content_subtype = 'html'
                email.body = tekst_iz_textarea_www
                
                email.send()
                context={"info_tekst":info_tekst, 
                 "email":email, 
                 "pokazi_textarea_infotext": pokazi_textarea_infotext,
                 "submitted": submitted}
            
            

            else:  # Ni email naslova, zato se vrni
                return HttpResponseRedirect("/form_vnos_update_availability")

        
            
    
    else: # GET
        
        context={"info_tekst":info_tekst, 
                 "email":email, 
                 "pokazi_textarea_infotext": pokazi_textarea_infotext,
                 "submitted": submitted}
    return HttpResponse(template.render(context, request))
    

def updateIzSeznama(request, id):

    gost = VnosGostov.objects.get(id=id, status_rez="rezervirano")
    obDatum = gost.od
    tipSobe = gost.tip
    listSob = seznamSob(tipSobe)
    
    # queryset >> pandas
    queryset = VnosGostov.objects.filter(status_rez="rezervirano")
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    
    IzdelavaGrafa(df_data, pd.to_datetime(obDatum, format="%d.%m.%Y"),
                  "R_Optimi")  # naredi tabelo, ki jo shrani v dbase
    rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                      "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                      "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27")
    template = loader.get_template("form_update.html")
    form = VnosRezForm(request.POST, instance=gost)

    if request.method == 'POST':
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            # return HttpResponseRedirect(template, gost.id)
            return HttpResponseRedirect("/form_rezervacije")
        else:
            print("Form ni VALID")
    else:  # GET
        form = VnosRezForm(instance=gost)

    context = {"rezervacije": rezervacije,
               "forma": form, "gost": gost, "listSob": listSob}
    return HttpResponse(template.render(context, request))


def delete_gost(request, id):
    gost = VnosGostov.objects.get(id=id, status_rez="rezervirano")
    template = loader.get_template("form_delete.html")
    if request.method == "POST":
        gost.status_rez="odpovedano"  #delete()
        gost.datum_odpovedi_dt = datetime.now()
        gost.save()
        return HttpResponseRedirect("/form_rezervacije")

    context = {"item": gost}
    return HttpResponse(template.render(context, request))


def form_graf(request):
    # pridobi podatke iz arhiva rezervacij
    # sosed FORM_GRAF.py  #"R_Optimi"))   "DN")) R_Optimi_iskanjeRez
    

    # Briši vse instance v database Graf
    Graf.objects.all().delete()
    # queryset >> pandas
    queryset = VnosGostov.objects.filter(status_rez="rezervirano")
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    df_graf= IzdelavaGrafa(df_data, pd.to_datetime("today"), "R_Optimi")
    print(df_graf)
    # Pretvori Padas >> Queryset
    my_dict = df_graf.to_dict(orient="records")
    my_instances = [Graf(**d) for d in my_dict]
    Graf.objects.bulk_create(my_instances)
    danes_dat = dt.date.today().strftime("%d.%m.%Y")
    

    if request.method == "POST":
        formular = izborDatuma(request.POST)
        if formular.is_valid():
            # cleaned_data da dobiš vrednost forma po submitu v views.py
            datum = formular.cleaned_data['datum']
            tipSobe = formular.cleaned_data['tipSobe']
            
            # Briši vse instance v database Graf
            Graf.objects.all().delete()
            # queryset >> pandas
            queryset = VnosGostov.objects.filter(status_rez="rezervirano")
            data = list(queryset.values())
            df_data = pd.DataFrame.from_records(data=data)
            df_graf = IzdelavaGrafa(df_data, pd.to_datetime(datum), "R_Optimi")
            # Pretvori Padas >> Queryset
            my_dict = df_graf.to_dict(orient="records")
            my_instances = [Graf(**d) for d in my_dict] #** is used to unpack a dictionary. In the given code, it is used to unpack each dictionary d in my_dict and pass its key-value pairs as arguments to the constructor of the class Rezervacija.
            Graf.objects.bulk_create(my_instances)
            rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                              "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                              "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")
            
            
            
            listSob = seznamSob(tipSobe)  # sosed RAZNO.py
            template = loader.get_template("form_graf.html")
            context = {"rezervacije": rezervacije,
                       "formDatum": formular, 
                       "listSob": listSob,
                       "danes_dat":danes_dat}
            return HttpResponse(template.render(context, request))

    else:
        formular = izborDatuma(
            data={"datum": pd.to_datetime("today").strftime(format="%d.%m.%Y")})

        # rezervacije = Graf.objects.all().values()
        rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                          "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                          "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")

        listSob = seznamSob("vse")
        
        context = {"rezervacije": rezervacije,
                   "formDatum": formular, 
                   "listSob": listSob,
                   "danes_dat": danes_dat}
        template = loader.get_template("form_graf.html")

        return HttpResponse(template.render(context, request))



def updateIzGrafa2(request, komande):
    #print(request.method)
    # print(request.POST)
    if isinstance(komande, int):
        id = komande
    else:
        razclemba = komande.split(sep="_")
        id = int(razclemba[0])

    gost = VnosGostov.objects.get(id=id, status_rez="rezervirano")
    tipSobe = gost.tip
    datumOD = gost.od
    stSobe = gost.stsobe
    
    

    rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                      "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                      "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")
    template = loader.get_template("form_update.html")
    form = VnosRezForm(request.POST, instance=gost)
    

    if request.method == 'POST':
        if form.is_valid():
            """In Django, when you access request.POST, it returns an immutable QueryDict object. 
            An immutable object means that its values cannot be modified directly. 
            However, if you need to modify the data, you can create a mutable copy of the QueryDict object.
            Creating a mutable copy allows you to modify the values within the copy without affecting the original QueryDict object. 
            It provides you with a way to make changes to the form data and assign it back to the form for further processing."""
            
            if "btn_update_rna" in request.POST:
                if form.cleaned_data['RNA'] == 'Avans':
                    # Create a mutable copy of the POST data
                    mutable_post_data = request.POST.copy()
                    # Clear the value of "zahteve" field in the mutable copy
                    mutable_post_data['RNA'] = 'AVANSOK'
                    # Create a new mutable QueryDict with the modified data
                    modified_post = QueryDict(mutable_post_data.urlencode(), mutable=True)
                    # Assign the modified QueryDict to the form's data attribute
                    form.data = modified_post
                    gost.RNA="AVANSOK"
                    gost.save()
                    
                    
                elif form.cleaned_data['RNA'] == 'NONref':
                    # Create a mutable copy of the POST data
                    mutable_post_data = request.POST.copy()
                    # Clear the value of "zahteve" field in the mutable copy
                    mutable_post_data['RNA'] = 'NONREFOK'
                    # Create a new mutable QueryDict with the modified data
                    modified_post = QueryDict(mutable_post_data.urlencode(), mutable=True)
                    # Assign the modified QueryDict to the form's data attribute
                    form.data = modified_post
                    gost.RNA="NONREFOK"
                    gost.save()
                    

                elif form.cleaned_data['RNA'] == 'ref':
                    # Create a mutable copy of the POST data
                    mutable_post_data = request.POST.copy()
                    # Clear the value of "zahteve" field in the mutable copy
                    mutable_post_data['RNA'] = 'refOK'
                    # Create a new mutable QueryDict with the modified data
                    modified_post = QueryDict(mutable_post_data.urlencode(), mutable=True)
                    # Assign the modified QueryDict to the form's data attribute
                    form.data = modified_post
                    gost.RNA="refOK"
                    gost.save()
                    
                    
                
            
            if "btn_brisi_zahteve" in request.POST:
                 # Create a mutable copy of the POST data
                mutable_post_data = request.POST.copy()
                # Clear the value of "zahteve" field in the mutable copy
                mutable_post_data['zahteve'] = ''
                # Create a new mutable QueryDict with the modified data
                modified_post = QueryDict(mutable_post_data.urlencode(), mutable=True)
            
                # Assign the modified QueryDict to the form's data attribute
                form.data = modified_post
                gost.zahteve=""
                gost.save()
                
                
            # Preveri, če nisi prenesel sobe na POLNO sobo pri optimizaciji
            errorMess = ""
            DatumODform = form.cleaned_data['od']
            DatumDOform = form.cleaned_data['do']
            TipSobeForm = form.cleaned_data['tip']
            StSobeForm = form.cleaned_data['stsobe']

            # Katere sobe naj bodo v grafu
            if "vse" in request.POST:
                listSob = seznamSob("vse")
            else:
                listSob = seznamSob(TipSobeForm)

            # Če želiš npr. prestaviti sobo s tipom C v sobo S
            #if request.POST.get("IzbrTipSobe") != "":
            #    TipSobeForm = request.POST.get("IzbrTipSobe")

            # Briši vse instance v GRAF
            #Graf.objects.all().delete()
            
            
             # queryset >> pandas  ARHIV GOSTOV
            queryset = VnosGostov.objects.filter(status_rez="rezervirano")
            data = list(queryset.values())
            df_data = pd.DataFrame.from_records(data=data)
            # queryset >> pandas  ŠIFRANT SOB
            queryset_sifrant = SifrantSob.objects.all()
            data = list(queryset_sifrant.values())
            df_sifrant_sob = pd.DataFrame.from_records(data=data)
            
            L_prosteSobe = proste_sobe(df_data, df_sifrant_sob, TipSobeForm, DatumODform, DatumDOform)
            #L_prosteSobe.append(99)
            
            
            # SAVE FORM
            
            # Prestavi sobo v drugo sobo oz. na obravnavni sobi shrani vse opravljene spremembe
            if StSobeForm in L_prosteSobe or StSobeForm == stSobe:  # or TipSobeForm == tipSobe:
                # S formom je vse ok, shrani ga
                form.save()
                # Briši vse instance v GRAF
                Graf.objects.all().delete()
                # queryset >> pandas  ARHIV GOSTOV
                queryset = VnosGostov.objects.filter(status_rez="rezervirano")
                data = list(queryset.values())
                df_data = pd.DataFrame.from_records(data=data)
                
                df_graf=IzdelavaGrafa(df_data, pd.to_datetime(datumOD, format="%d.%m.%Y"), "R_Optimi")
                #print(df_graf)
                # Pretvori Padas >> Queryset
                my_dict = df_graf.to_dict(orient="records")
                my_instances = [Graf(**d) for d in my_dict]
                Graf.objects.bulk_create(my_instances)

                rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                                  "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                                  "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")
                # V response na DNU tega modula dodaj Ok mess
                OkMess = "Formular je shranjen"
                context = {"IDstr": str(gost.id), "OkMess": OkMess, "forma": form,
                           "gost": gost, "rezervacije": rezervacije, "listSob": listSob}

            else: # Rezervacije ne moreš prestaviti v polno sobo
                errorMess = "Rezervacije ne moreš prestaviti v polno sobo, OZ prestavljaš v drug TIP sobe"
                context = {"IDstr": str(gost.id), "errorMess": errorMess, "forma": form,
                           "gost": gost, "rezervacije": rezervacije, "listSob": listSob}
            
        else:  # FORM NI VALID
            TipSobeForm = form.cleaned_data['tip']
            listSob = seznamSob(TipSobeForm)
            context = {"forma": form, "gost": gost,
                       "rezervacije": rezervacije, "listSob": listSob}
            print("Form ni VALID")

    else:  # GET
        form = VnosRezForm(instance=gost)
        tipSobe = gost.tip
        DatumTabela = datumOD

        DatumIzTabele = request.GET.get("datumTabela")
        if DatumIzTabele == "":
            DatumIzTabele = datumOD

        if datumOD != DatumIzTabele and DatumIzTabele != None:
            DatumTabela = DatumIzTabele
        
        
        if "naprej" in request.GET:
            DatumTabela = pd.to_datetime(
                DatumTabela, format="%d.%m.%Y") + pd.Timedelta(days=7)
            datumOD = DatumTabela
            DatumTabela = DatumTabela.strftime("%d.%m.%Y")
        elif "nazaj" in request.GET:
            DatumTabela = pd.to_datetime(
                DatumTabela, format="%d.%m.%Y") - pd.Timedelta(days=7)
            datumOD = DatumTabela
            DatumTabela = DatumTabela.strftime("%d.%m.%Y")
        
        
        if "vse" in request.GET:
            listSob = seznamSob("vse")
            tipSobe = "vse"
        else:
            listSob = seznamSob(tipSobe)
            
        
        # Briši vse instance v database Graf
        Graf.objects.all().delete()
        # queryset >> pandas
        queryset = VnosGostov.objects.filter(status_rez="rezervirano")
        data = list(queryset.values())
        df_data = pd.DataFrame.from_records(data=data)
        df_graf= IzdelavaGrafa(df_data, pd.to_datetime(datumOD, format="%d.%m.%Y"), "R_Optimi")
        
        # Pretvori Padas >> Queryset
        my_dict = df_graf.to_dict(orient="records")
        my_instances = [Graf(**d) for d in my_dict]
        Graf.objects.bulk_create(my_instances)
        
        
        
        rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                          "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                          "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")

        context = {"forma": form, "DatumTabela": DatumTabela, "gost": gost,
                   "IDstr": str(gost.id), "rezervacije": rezervacije,
                   "listSob": listSob, "IzbrTipSobe": tipSobe,
                   }

    return HttpResponse(template.render(context, request))


def virtual(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_AgencijaVirtual.json')

    form = IzborAgencije(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            vrstaAgencije = form.cleaned_data['vrstaAgencije']

            jsonData = odpriJson(js_file=js_file)  # Sosed: Razno.py
            agencijaJson = jsonData[0]

            if agencijaJson != vrstaAgencije:
                # Shrani to agencijo v json
                jsonData[0] = vrstaAgencije

                # Sosed: Razno.py
                shraniJson(js_file=js_file, jsonData=jsonData)

            else:
                vrstaAgencije = agencijaJson

            virtualRez = VnosGostov.objects.filter(RNA="ExpColl", agencija=vrstaAgencije, status_rez="rezervirano").order_by("od_dt")
            paginator = Paginator(virtualRez,10)
            page_number = request.GET.get('page')
            virtualRez = paginator.get_page(page_number)
            
            
            
            template = loader.get_template("form_virtual.html")
            context = {"virtualRez": virtualRez, "forma": form}

            return HttpResponse(template.render(context, request))

    else:  # GET
        jsonData = odpriJson(js_file=js_file)  # Sosed: Razno.py
        vrstaAgencije = jsonData[0]
        form = IzborAgencije(data={"vrstaAgencije": vrstaAgencije})
        # Sorting Sortiranje in pretvarjanje datuma iz string v datetime.datetime.strptime
        virtualRez = VnosGostov.objects.filter(RNA="ExpColl", agencija=vrstaAgencije, status_rez="rezervirano").order_by("od_dt")
        paginator = Paginator(virtualRez,10)
        page_number = request.GET.get('page')
        virtualRez = paginator.get_page(page_number)
        
        
        
        template = loader.get_template("form_virtual.html")
        context = {"virtualRez": virtualRez, "forma": form}
        return HttpResponse(template.render(context, request))


def virtual_podrobno(request, id):
    record = VnosGostov.objects.get(id=id, status_rez="rezervirano")
    template = loader.get_template('form_virt_podrobno.html')
    
    if request.method == "POST":
        msg=""
        if "status_ok" in request.POST:
            if record.AvansEUR == "":
                record.AvansEUR = None
            if record.IDponudbe == "":
                record.IDponudbe = None
            record.RNA = "NONREFOK"
            msg = "Račun je PLAČAN!"
            record.save()
        elif "poslji_racun" in request.POST:
            record.RNA = "racun poslan " + datetime.strftime(datetime.now(), "%d.%m.")
            record.save()
            msg = "Račun je bil poslan!"
        elif "undo" in request.POST:
            record.RNA = "ExpColl"
            record.save()
            msg = "Status se ni spremenil"
        context = {"rezervacija": record, "msg": msg}
        #return HttpResponseRedirect("/form_virtual")
    
    else: # GET
        context = {"rezervacija": record}
    
    return HttpResponse(template.render(context, request))


def virtual_spremeni_status(request, id):
    record = VnosGostov.objects.get(id=id, status_rez="rezervirano")
    if record.AvansEUR == "":
        record.AvansEUR = None
    if record.IDponudbe == "":
        record.IDponudbe = None

    record.RNA = "NONREFOK"
    #record.save()

    return HttpResponseRedirect("/form_virtual")

############### PONUDBA ################

# Začetni formular, kjer izbereš osnovne podatke in jih shraniš v Json
def ponudba_faza_1(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')

    if request.method == "POST":
        form = IzborDatumovPonudba(request.POST)
        if form.is_valid():
            jezik = form.cleaned_data['jezik']
            vrstaInAli = form.cleaned_data['vrstaInAli']
            odDatum = form.cleaned_data['od']
            doDatum = form.cleaned_data['do']
            ime = form.cleaned_data['ime']
            email = form.cleaned_data['email']
            rna = form.cleaned_data['rna']
            avans = form.cleaned_data['avans']
            odpoved = form.cleaned_data['odpoved']


            dictVhodovPonudba = {'jezik': jezik, 'vrstaInAli': vrstaInAli, 'od': odDatum, 'do': doDatum,
                                 'ime': ime, 'email': email, 'rna': rna, 'avans': avans, 'odpoved': odpoved,}
            # Sosed: Razno.py
            shraniJson(js_file=js_file, jsonData=dictVhodovPonudba)

            # shrani datuma, ime, email... v Json
            # pojdi na naslednjo fazo
            # izračun prostih sob po tipih

            # return HttpResponse(template.render(context, request))
            return HttpResponseRedirect("/form_ponudba_faza_1/form_ponudba_faza_2")
        else:
            print("form ni izpolnjen v celoti")

    else:  # GET
        form = IzborDatumovPonudba()
        template = loader.get_template("form_ponudba_faza_1.html")
        context = {"forma": form}
        return HttpResponse(template.render(context, request))


# Kreiraj tabelo, kjer izbereš tip sobe, št oseb, št sob
def ponudba_faza_2(request: Any) -> HttpResponse:
    """
    View function that displays a list of rooms and their availability for a given date range.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object that contains the rendered template.
    """
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')
    dictVhodovPonudba = odpriJson(js_file=js_file)  # Sosed: Razno.py
    odDatum = dictVhodovPonudba["od"]
    doDatum = dictVhodovPonudba["do"]
    jezik = dictVhodovPonudba["jezik"]
    
    # k sosedu po dict dodatnih zahtev glede na izbrani jezik
    dict_zahteve = dodatne_zahteve(jezik=jezik)
    
     # queryset >> pandas  ARHIV GOSTOV
    queryset = VnosGostov.objects.filter(status_rez="rezervirano")
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    # queryset >> pandas  ŠIFRANT SOB
    queryset_sifrant = SifrantSob.objects.all()
    data = list(queryset_sifrant.values())
    df_sifrant_sob = pd.DataFrame.from_records(data=data)
    
    dictProstihSob = prosteSobeZaPonudbo(df_data, df_sifrant_sob, odDatum=odDatum, doDatum=doDatum)
    template = loader.get_template("form_ponudba_faza_2.html")
    context = {"dictProstihSob": dictProstihSob, 
               "dictVhodovPonudba": dictVhodovPonudba,
               "dict_zahteve":dict_zahteve}
    return HttpResponse(template.render(context, request))


# def brez templata >> samo pobere podatke iz tabele za določitev št oseb, otrok in cene in jih vnese v Json
def ponudba_tabela_sobe(request, tip) -> HttpResponseRedirect:
    # if request.method== "GET":
    # print(request.method)
    stOseb = request.POST.get(f'stOseb_{tip}')
    stOtrok = request.POST.get(f'stOtrok_{tip}')
    cena = request.POST.get(f'cena_{tip}')
    tipStCena = [stOseb, stOtrok, tip, cena]
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')
    dictVhodovPonudba = odpriJson(js_file=js_file)  # Sosed: Razno.py
    if "tipSobe" in dictVhodovPonudba:  # Pomeni, da je v dictu že ta Key
        L_tipov = list(dictVhodovPonudba["tipSobe"])
        L_tipov.append(tipStCena)
        dictVhodovPonudba["tipSobe"] = L_tipov
    else:
        dictVhodovPonudba["tipSobe"] = [tipStCena]

    shraniJson(js_file=js_file, jsonData=dictVhodovPonudba)  # Sosed: Razno.py

    # Vrni se nazaj na izbiro sob
    return HttpResponseRedirect("/form_ponudba_faza_1/form_ponudba_faza_2")
   

# Gumb, ki shrani ponudbo v DB
def ponudba_shrani(request):
    zahteve = request.POST.get('dodatne_zahteve')
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')
    dictVhodovPonudba = odpriJson(js_file=js_file)  # Sosed: Razno.py
    # v dict dodaj dodatne zahteve
    dictVhodovPonudba["zahteve"] = zahteve
    shraniJson(js_file=js_file, jsonData=dictVhodovPonudba)  # Sosed: Razno.py

    # Prenesi podatke o ponudbi v database
    datumVnosa = pd.to_datetime("today").strftime(format=("%d.%m.%Y"))

        # Preveri, ali si sploh izbral kakšno sobo:
    if dictVhodovPonudba.get("tipSobe") is None:  # !!!!!
        print("ni izbranih sob")

    else:
        L_steviloSob = len(dictVhodovPonudba["tipSobe"])
        # rabiš, da veš ali gre za MR - če je LsteviloSob >1 ali če je v tipSobe stSob>1 -->> MR
        vrstaInAli = dictVhodovPonudba["vrstaInAli"]
        # print(L_steviloSob)
        # ugotovi MR:
        if L_steviloSob > 1 and vrstaInAli == "IN":
            js_file = os.path.join(
                settings.BASE_DIR, 'Rezervacije//static//json//ponudbaStevecMR.json')
            stevec = odpriJson(js_file=js_file)  # Sosed: Razno.py
            multiroom = stevec+1
            stevec = stevec + 1
            shraniJson(js_file=js_file, jsonData=stevec)  # Sosed: Razno.py
        else:
            multiroom = ""
            # Naredi INSTANCO posamezne sobe- če je v dictu več sob, narediš za vsako sobo svojo instanco- FOR
        for i in range(0, L_steviloSob):
            record = Ponudba(datumVnosa=datumVnosa,
                             status="1_Poslano",
                             jezik=dictVhodovPonudba["jezik"],
                             ime=dictVhodovPonudba["ime"],
                             od=dictVhodovPonudba["od"],
                             do=dictVhodovPonudba["do"],
                             email=dictVhodovPonudba["email"],
                             rna=dictVhodovPonudba["rna"],
                             avans=dictVhodovPonudba["avans"],
                             odpoved=dictVhodovPonudba["odpoved"],
                             stOdr=dictVhodovPonudba["tipSobe"][i][0],
                             stOtr=dictVhodovPonudba["tipSobe"][i][1],
                             tip=dictVhodovPonudba["tipSobe"][i][2],
                             cena=dictVhodovPonudba["tipSobe"][i][3],
                             multiroom=multiroom,
                             zahteve=zahteve
                             )
            record.save()
        #ponudbaHtml(dictPonudba=dictVhodovPonudba)
        # print(ponudbaHtml)
        return HttpResponseRedirect("/form_ponudba_predogled")

    return HttpResponseRedirect("/form_ponudba_faza_1/form_ponudba_faza_2")

    # Vzorec instance !!!!!
    # person = Person(name=my_data['name'], age=my_data['age'], email=my_data['email'])
    # person.save()

# Predogled pred pošiljanjem. Trenuto je še aplikacija za urejanje rich-teksta
def ponudba_predogled(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')
    dictVhodovPonudba = odpriJson(js_file=js_file)  # Sosed: Razno.py
    htmlTekst= ponudba_izdelava_Html(dictPonudba=dictVhodovPonudba)
    context= {"htmlTekst": htmlTekst, 'api_key': env("API_texteditor")} # poglej v .env za api key
    template = loader.get_template("form_ponudba_predogled.html")
    return HttpResponse(template.render(context, request))


# Gumb za pošiljanje ponudbe na email
def ponudba_poslji(request):
    modificiran_html = request.POST.get("html_text")
    email = EmailMessage(subject="Ponudba ", body= modificiran_html, from_email= settings.EMAIL_HOST_USER, to= [settings.RECIPIENT_ADDRESS,]
                    )
    # Set the HTML version of the message
    email.content_subtype = 'html'
    email.body = modificiran_html
    print(modificiran_html)
    
    email.send()
    return HttpResponseRedirect("/form_ponudba_seznam")


# Pri kreiranju ponudba imaš več oken, na oknu za predogled ponudbe je možno izbrisati sobo iz ponudbe
def ponudba_brisi_sobo(request, id_sobe):
    print(id_sobe-1)
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')
    dictVhodovPonudba = odpriJson(js_file=js_file)  # Sosed: Razno.py
    del dictVhodovPonudba["tipSobe"][id_sobe-1]
    shraniJson(js_file=js_file, jsonData=dictVhodovPonudba)  # Sosed: Razno.py

    return HttpResponseRedirect("/form_ponudba_faza_1/form_ponudba_faza_2")


# Seznam vseh ponudb, pod tabelo imaš gumbe za različne prikaze: Arhiv, vse ponudbe, aktivne,...
def ponudba_seznam(request):
    # Ponudbam, ki so starejše od 2 dni, spremeni status v 0_Nepotrjeno
    arhiv_starih_ponudb = Ponudba.objects.filter(Q(datumVnosa_dt__lt=datetime.now().date()-timedelta(days=1)) & Q(status ="1_Poslano"))
    arhiv_starih_ponudb.update(status = "0_Nepotrjeno")
    template=loader.get_template("form_ponudba_seznam.html")
    if request.method == "POST":
        if "pokazi_arhiv" in request.POST:
            ponudbe = Ponudba.objects.filter(status__in=["0_Nepotrjeno"])
        if "aktivne_ponudbe" in request.POST:
            ponudbe = Ponudba.objects.filter(status__in=["1_Poslano", "2_1_Vneseno"])
        if "vse_ponudbe" in request.POST:
            ponudbe = Ponudba.objects.filter(status__in=["0_Nepotrjeno", "1_Poslano", "2_1_Vneseno", "3_Hvala"])
        paginator = Paginator(ponudbe,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={"ponudbe": ponudbe, "page_obj": page_obj}
    else:
        ponudbe = Ponudba.objects.filter(status__in=["1_Poslano", "2_1_Vneseno"])
        paginator = Paginator(ponudbe,10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        
        context={"ponudbe": ponudbe, "page_obj": page_obj}
        
        
    
    
    return HttpResponse(template.render(context,request))


####################################

# Obdelava ponudb v seznamu> potem, ko izbereš ponudbo iz seznama >> - Ali gre za potrditev, zahvalo, opomin.
def ponudba_obdelava(request, id):
    template = loader.get_template("form_ponudba_obdelava.html")
    ponudba = Ponudba.objects.get(id=id)
    form= PonudbaForm(request.POST, instance=ponudba)
    
    
    if request.method == 'POST':
        if "update_knof" in request.POST:
            if form.is_valid():
                form.save()
                ponudba = Ponudba.objects.get(id=id)
                # Po update vedno spremeni datum vnosa na Danes, da se v seznamu spet ne spremeni status v 0 , (ker se po xx dneh status spremeni avtomatsko)
                ponudba.datumVnosa = dt.date.today().strftime("%d.%m.%Y")
                #ponudba.datumVnosa_dt = dt.date.today()  # !!!!!>>NI treba, ker je v Models.py definirano, da se datumVnosa avtomatsko pretvori v datumVnosa_dt
                ponudba.save() 
                return HttpResponseRedirect("/form_ponudba_seznam")
                #OkMess = "Formular je shranjen"
            else:
                OkMess  = "Formular NI Shranjen"
            context={"OkMess": OkMess, "forma": form}
            return HttpResponse(template.render(context, request))

        if "delete_knof" in request.POST:
            ponudba.delete()
        
            return HttpResponseRedirect("/form_ponudba_seznam")
    
        if "potrditev_knof" in request.POST or "hvala_knof" in request.POST:
            # Preveri ali je multiroom>> če je, naredi list vseh sob v MR-ju
            my_dict = dict(request.POST.items())  # Vrne dict iz templateja
            
            if ponudba.multiroom != "":  # Tu gre za Multiroom
                st_multirooma = ponudba.multiroom
                qset_multiroom_sobe = Ponudba.objects.filter(multiroom=st_multirooma)
                # Spremeni status MR sobam v Ponudba
                # Update multiple database records s Querysettom !!!!!
                if "hvala_knof" in request.POST:
                    qset_multiroom_sobe.update(status = "3_Hvala")
                    my_dict = list(qset_multiroom_sobe.values()) #!!!!! izdelava list of dicts iz queryset-a
                else: # 2
                    qset_multiroom_sobe.update(status = "2_Potrjeno")
                    # List of dicts:
                    my_dict = list(qset_multiroom_sobe.values()) #!!!!! izdelava list of dicts iz queryset-a
                    
                    # Če gre za Avans v MR, potem naj ima samo 1. record Avans, ostali pa refOK
                    if my_dict[0]["rna"]== "Avans":
                        st_sob_v_MR = len(my_dict)
                        for x in range(1,st_sob_v_MR):
                            ponudba_rna_id = my_dict[x]["id"]
                            ponudba_rna = Ponudba.objects.get(id=ponudba_rna_id)
                            ponudba_rna.rna ="refOK"
                            ponudba_rna.save()
                        


            else: # Tu gre za MonoRoom
                if "hvala_knof" in request.POST:
                    ponudba.status ="3_Hvala"
                    if ponudba.rna =="Avans":
                        #rezervacija = VnosGostov Moraš najeprej pri vnosu rezervacij iz ponudbe vnesti še ID ponudbe, da lagko lociraš NONREF oz AVANSOK....
                        ponudba.rna ="AVANSOK"
                    elif ponudba.rna =="Nonref":
                        ponudba.rna ="NONREFOK"
                else:
                    ponudba.status ="2_Potrjeno"
                ponudba.save() 
                # Pretvorba Single Instance (get) v DICT >> model_to_dict -> moraš narediti import !!!!!
                my_dict = [model_to_dict(ponudba)]
            
            js_file = os.path.join(
                settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_ponudba_obdelava.json')
            
            http_odgovor, sklic, rna, rokPlacila = ponudba_obdelava_Html(my_dict)
            # Če je Avans ali Nonref, v bazo shrani sklic
            if rna == "Nonref" or rna == "Avans":
                id_ponudbe = my_dict[0]["id"]
                ponudba1 = Ponudba.objects.get(id=id_ponudbe)
                ponudba1.sklic = sklic
                ponudba1.rokPlacilaAvansa= datetime.strptime(rokPlacila, "%d.%m.%Y")
                ponudba1.save()

            # Shrani http tekst v json, da ga boš odprl v form pon obd predogl
            shraniJson(js_file=js_file, jsonData=http_odgovor)
            

            return HttpResponseRedirect("/form_ponudba_obd_predogl")
        
        
    
    
    
    else:   # GET
        ponudba = Ponudba.objects.get(id=id)
        form = PonudbaForm(instance= ponudba)
        
        context= {"forma": form}
        template = loader.get_template("form_ponudba_obdelava.html")

    return HttpResponse(template.render(context,request))

# Zadnja faza_ predogled tekstov pred pošiljanjem
def ponudba_obdelava_teksti(request): 
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_ponudba_obdelava.json')
            
    
    html_tekst = odpriJson(js_file=js_file)
    
    template = loader.get_template("form_ponudba_obd_predogl.html")
    context = {"htmlTekst": html_tekst}
    return HttpResponse(template.render(context,request))



def ponudba_obdelava_poslji(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_ponudba_obdelava.json')
    html_tekst = odpriJson(js_file=js_file)
    email = EmailMessage(subject="Ponudba ", body= html_tekst, from_email= settings.EMAIL_HOST_USER, recipient_list=[settings.RECIPIENT_ADDRESS])
    #print(html_tekst)                
    # Set the HTML version of the message
    email.content_subtype = 'html'
    email.body = html_tekst
    
    email.send()
    return HttpResponseRedirect("/form_ponudba_seznam")

# Vnesi rezervacijo iz ponudbe
def ponudba_vnos_iz_ponudbe(request, id):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    ponudba = Ponudba.objects.get(id=id)
    
    if ponudba.stOdr =="":
        ponudba.stOdr = 0
    if ponudba.stOtr =="":
        ponudba.stOtr = 0
    

    # IZDELAVA LISTA PROSTIH SOB
    # queryset >> pandas
    queryset = VnosGostov.objects.filter(status_rez="rezervirano")
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    # queryset >> pandas
    queryset_sifrant = SifrantSob.objects.all()
    data = list(queryset_sifrant.values())
    df_sifrant_sob = pd.DataFrame.from_records(data=data)
    
    
    L_prosteSobe = proste_sobe(df_data, df_sifrant_sob, ponudba.tip, ponudba.od, ponudba.do)
    
    odpriJson(js_file=js_file)
   
    jsonData= {}
    jsonData["vrsta"]= "avtovnos"
    jsonData["cena"] = ponudba.cena
    jsonData["ime"] = ponudba.ime
    jsonData["agencija"] = "Nasi"
    jsonData["od"] = ponudba.od
    jsonData["do"] = ponudba.do
    jsonData["rna"] = ponudba.rna
    jsonData["avans_eur"]= ponudba.avans
    jsonData["email"] = ponudba.email
    jsonData["list_prostih_sob"] = L_prosteSobe
    jsonData["tip"] = ponudba.tip
    jsonData["id_ponudbe"] = id
    jsonData["stsobe"] = L_prosteSobe[0]
    jsonData["stoseb"]= str(int(ponudba.stOdr)+int(ponudba.stOtr))
    jsonData["zahteve"]= ""
    jsonData["drzava"]= ""
    if ponudba.rokPlacilaAvansa == None:
        jsonData["rok_placila_avansa"]= None
    else:
        jsonData["rok_placila_avansa"]= datetime.strftime(ponudba.rokPlacilaAvansa,"%d.%m.%Y")

    shraniJson(js_file=js_file, jsonData=jsonData)
    # Spremeni status ponudbe, ki si jo poslal gostu:
    ponudba.status = "2_1_Vneseno"
    ponudba.save()
    return HttpResponseRedirect("/form_vnos_rocni")
   

def dashboard(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//dash_datum_raport.json')
    
    template = loader.get_template("form_dashboard.html")
    danes = datetime.now().date()
    jutri = danes+ timedelta(days=1)
    letos = danes.year
    # Zberi podatke iz Vnos-a kot QS, in jih pretvori v DF, ki ga pošlješ k sosedu dashboard.py >> querset to pandas
    queryset = VnosGostov.objects.filter(status_rez="rezervirano")
    queryset_odpovedi = VnosGostov.objects.filter(status_rez="odpovedano")

    data = list(queryset.values())
    df_data_rezervirano = pd.DataFrame.from_records(data=data)

    data = list(queryset_odpovedi.values())
    df_data_odpovedano = pd.DataFrame.from_records(data=data)
    
    df_podatki= Dashboard(df_data_rezervirano,df_data_odpovedano, letos)
    # NOČITVE
    df_nocitve = df_podatki.nocitve_in_eur_po_mescih()

    # PROFIT PO AGENCIJAH
    df_profit_agencije = df_podatki.profit_po_agencijah()
    
    
    # LISTA GOSTOV
    lista_gostov = df_podatki.lista_gostov_danes()

    # PROSTE SOBE DANES
    proste_sobe_danes = df_podatki.proste_sobe_danes()
    
    # ZADNJE REZERVACIJE
    zadnje_rezervacije= df_podatki.zadnje_rezervacije_danes()
    
    # ZADNJE ODPOVEDI
    zadnje_odpovedi = df_podatki.zadnje_odpovedi_danes()
    # print(zadnje_rezervacije)

    # ID PONUDB
    id_ponudb = Ponudba.objects.filter(status = "2_Potrjeno").values("id", "ime")
    # Izdelaj list samo 1 stolpca v QS: !!!!!
    id_ponudb = list(id_ponudb.values_list("id", "ime"))# flat=True))
    #print(id_ponudb)
    # CCD AVANSI
    avansi = VnosGostov.objects.filter(Q(status_rez = "rezervirano") & Q(RNA="Avans")).values("id", "imestranke", "stsobe", "RokPlacilaAvansa") 
    # SKUPAJ EUR (Raport)
    #  T_RaportVsi=IzdelavaGrafa(self.datumRaport,"DN") # SOSED graf2
    #  T_RaportIzbDan=T_RaportVsi.iloc[-5:,51].to_frame(name="Podatki").reset_index()
    #  T_RaportIzbDan["Podatki"]=T_RaportIzbDan["Podatki"].astype(int)
    raport = IzdelavaGrafa(df_data= df_data_rezervirano, 
                           DatumObravnave= pd.Timestamp(jutri), 
                           Vir= "raport")
    
    
    if request.method == "POST":
        if "btn_danes" in request.POST:
            raport = IzdelavaGrafa(df_data= df_data_rezervirano, 
                           DatumObravnave= pd.Timestamp(danes), 
                           Vir= "raport")
            shraniJson(js_file=js_file, jsonData=datetime.strftime(danes, "%d.%m.%Y"))  

        if "btn_jutri" in request.POST:
            raport = IzdelavaGrafa(df_data= df_data_rezervirano, 
                           DatumObravnave= pd.Timestamp(jutri), 
                           Vir= "raport")
            shraniJson(js_file=js_file, jsonData=datetime.strftime(jutri, "%d.%m.%Y"))        

        
        if "btn_dan_nazaj" in request.POST:
            zadnji_datum = odpriJson(js_file= js_file)
            zadnji_datum_dt = datetime.strptime(zadnji_datum, "%d.%m.%Y") - timedelta(days=1)
            raport = IzdelavaGrafa(df_data= df_data_rezervirano, 
                           DatumObravnave= pd.Timestamp(zadnji_datum_dt), 
                           Vir= "raport")
            shraniJson(js_file=js_file, jsonData=datetime.strftime(zadnji_datum_dt, "%d.%m.%Y"))
        
        if "btn_dan_naprej" in request.POST:
            zadnji_datum = odpriJson(js_file= js_file)
            zadnji_datum_dt = datetime.strptime(zadnji_datum, "%d.%m.%Y") + timedelta(days=1)
            raport = IzdelavaGrafa(df_data= df_data_rezervirano, 
                           DatumObravnave= pd.Timestamp(zadnji_datum_dt), 
                           Vir= "raport")
            shraniJson(js_file=js_file, jsonData=datetime.strftime(zadnji_datum_dt, "%d.%m.%Y"))

        
        stevilka_dneva_datuma = odpriJson(js_file=js_file)
        stevilka_dneva_datuma = datetime.strptime(stevilka_dneva_datuma, "%d.%m.%Y").weekday()
        
        ime_dneva_datuma = ime_dneva_v_tednu(st_dneva=stevilka_dneva_datuma)
        
        
    else:   # GET
        shraniJson(js_file=js_file,jsonData= datetime.strftime(jutri, "%d.%m.%Y"))
        stevilka_dneva_datuma = jutri.weekday()
        ime_dneva_datuma = ime_dneva_v_tednu(st_dneva=stevilka_dneva_datuma)
        
    
    
    context={"df_nocitve":df_nocitve, "id_ponudb":id_ponudb, 
            "lista_gostov": lista_gostov, 
            "proste_sobe": proste_sobe_danes,
            "zadnje_rezervacije": zadnje_rezervacije,
            "zadnje_odpovedi": zadnje_odpovedi,
            "agencije_profit": df_profit_agencije,
            "avansi": avansi,
            "raport": raport,
            "ime_dneva_v_tednu": ime_dneva_datuma,
            }
    return HttpResponse(template.render(context, request))



def bar(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//bar.json')
    
    # print(request.method)
    # print(request.POST.get)
    template = loader.get_template("form_bar.html")
    cenik = Bar_cenik.objects.all()
    forma  = Bar_form()    
    if request.method == "POST":
        #context={"forma":forma}
        
        # Izberi sobo in s tem dobiš value = id gosta
        if "btn_st_sobe" in request.POST: 
            id = request.POST["soba"]
            print(id)
            gost = VnosGostov.objects.get(id=id)
            gostova_narocila = Bar_narocila.objects.select_related("gost").filter(gost=id)
            context={"forma":forma, "cenik": cenik, "gost":gost, "gostova_narocila": gostova_narocila}
            js_data = {"id": gost.id, "imestranke": gost.imestranke}
            shraniJson(js_file=js_file, jsonData=js_data)

        if "btn_brisi_artikel" in request.POST:
            js_data= odpriJson(js_file=js_file)
            id_gost = js_data["id"]
            gost = VnosGostov.objects.get(id=id_gost)
            id = request.POST["btn_brisi_artikel"]
            gostovo_narocilo = Bar_narocila.objects.get(id=id)
            print(gostovo_narocilo)
            gostovo_narocilo.delete()
            
            gostova_narocila = Bar_narocila.objects.select_related("gost").filter(gost=id_gost)
            context={"forma":forma, "cenik": cenik, "gost":gost, "gostova_narocila": gostova_narocila}

        # Izbereš artikel v "gumbnem seznamu"
        if "btn_artikel" in request.POST:
            js_data= odpriJson(js_file=js_file)
            id_gost = js_data["id"]
            gost = VnosGostov.objects.get(id=id_gost)
            artikel_id = request.POST["btn_artikel"]
            artikel = cenik.get(id=artikel_id)
            
            # Dodaj artikel v json
           # if ("artikli") not in js_data:
            js_data["id_artikla"]= artikel.id
            js_data["cena_artikla"]=float(artikel.cena)
            #    shraniJson(js_file=js_file, jsonData=js_data)
            # else:
            #     js_data["artikli"].append((artikel.id, float(artikel.cena)))
                
            shraniJson(js_file=js_file, jsonData=js_data)
            
            context={"forma":forma,"cenik": cenik, 
                     "gost":gost, "artikel":artikel}
        
        # Spodnja dva ifa sta ista- prvi je za ročni vnos količine, drugi z gumbi
        if "btn_izracun_artikla" in request.POST:
            stevilo_artiklov = request.POST.get("st_artiklov")
            js_data= odpriJson(js_file=js_file)
            id_gost = js_data["id"]
            gost = VnosGostov.objects.get(id=id_gost)
            if "id_artikla" not in js_data or stevilo_artiklov=="": 
                error_msg = "Ni izbranega artikla!"
                context={"forma": forma, 
                         "cenik": cenik, 
                         "gost": gost, 
                         "error_msg": error_msg}
            else:
                id_artikla = js_data["id_artikla"]
                artikel = cenik.get(id=id_artikla)
                cena_artiklov = js_data["cena_artikla"] * int(stevilo_artiklov)
                # cena_artiklov= round(cena_artiklov,2)
               
                Bar_narocila.objects.create(gost=gost, artikel= artikel, kolicina= stevilo_artiklov)
                gostova_narocila = Bar_narocila.objects.select_related("gost").filter(gost=id_gost)
                context={"forma":forma,"cenik": cenik, 
                        "gost":gost, "artikel":artikel, 
                        "cena_artiklov":cena_artiklov,
                        "gostova_narocila":gostova_narocila}
        
        if "btn_stevilka" in request.POST:
            stevilo_artiklov = request.POST.get("btn_stevilka")
            js_data= odpriJson(js_file=js_file)
            id_gost = js_data["id"]
            gost = VnosGostov.objects.get(id=id_gost)
            if "id_artikla" not in js_data:
                error_msg = "Ni izbranega artikla!"
                context={"forma": forma, 
                         "cenik": cenik, 
                         "gost": gost, 
                         "error_msg": error_msg}
            else:
                error_msg =""
                id_artikla = js_data["id_artikla"]
                artikel = cenik.get(id=id_artikla)
                cena_artiklov = js_data["cena_artikla"] * int(stevilo_artiklov)
                # cena_artiklov= round(cena_artiklov,2)
                Bar_narocila.objects.create(gost=gost, artikel= artikel, kolicina= stevilo_artiklov)
                gostova_narocila = Bar_narocila.objects.select_related("gost").filter(gost=id_gost)
                """Test_vsi_fildi = Bar_narocila.objects.select_related("gost").all()
                for c in Test_vsi_fildi:
                    print(c.gost.SO)"""
                context={"forma":forma,"cenik": cenik, 
                         "gost":gost, "artikel":artikel, 
                        "cena_artiklov":cena_artiklov, 
                        "error_msg": error_msg,
                        "gostova_narocila": gostova_narocila}
        



    else: # GET
        context={"forma":forma, "cenik": cenik}
    
    return HttpResponse(template.render(context, request))





def dn_podatki(request):
    js_file=js_file = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//dn_ob_datum.json')  
    podatki = VnosGostov.objects.filter(status_rez="rezervirano")
    template = loader.get_template("form_dn.html")
    forma = Dn_form_izberi_datum()
    
    if request.method=="POST":
        print(request.POST)
        
        ob_datum= odpriJson(js_file=js_file)
        ob_datum = datetime.strptime(ob_datum, "%d.%m.%Y")
        
        ###____###
        data = Dn_izracuni(podatki=podatki, ob_datum= ob_datum)
        prihodi = data.prihodi()
        odhodi = data.odhodi()
        stayover = data.stayover()
        menjave = data.menjave()
        ###____###
        
        
        podatki_za_racune = data.podatki_za_racune() # Dict podatkov vseh sob za ta dan
        #print(podatki_za_racune)
        # Povozi današnji datum in v json vnese datum , ki si ga izbereš iz datepickerja:
        if "btn_datum_dn" in request.POST or  "btn_datum_danes" in request.POST or  "btn_datum_jutri" in request.POST:
            if "btn_datum_dn" in request.POST:
                datum_dn_iz_template = request.POST.get("moj_datum")
                ob_datum= datetime.strptime(datum_dn_iz_template, "%Y-%m-%d")
            elif "btn_datum_danes" in request.POST:
                ob_datum= datetime.now().date()
            elif "btn_datum_jutri" in request.POST:
                ob_datum= (datetime.now()+ timedelta(days=1)).date()

            ob_datum_str= datetime.strftime(ob_datum, format="%d.%m.%Y")
            
            ###____###
            data = Dn_izracuni(podatki=podatki, ob_datum= ob_datum)
            prihodi = data.prihodi()
            odhodi = data.odhodi()
            stayover = data.stayover()
            menjave = data.menjave()
            ###____###


            # Shrani nov ob_datum v Json
            shraniJson(js_file=js_file, jsonData=ob_datum_str)
            forma = Dn_form_izberi_datum()
            context={"prihodi":prihodi, "odhodi":odhodi, 
                 "stayover":stayover, "menjave":menjave, 
                 "forma": forma, "ob_datum": ob_datum_str}
            return HttpResponse(template.render(context, request))

        if "btn_prenos_na_app" in request.POST:
            data_class = App_podatki(ob_datum= ob_datum, vir="app")
            data_class.PodatkiZaWebApplic()
            
            return HttpResponseRedirect("form_dn")


        if "gumb_preracunaj" in request.POST:
            ob_datum_str= odpriJson(js_file=js_file)
            st_sobe = request.POST.get("gumb_preracunaj")  # skup variabil: št. odr, št. otr, št. sobe
            st_odr = request.POST.get("st_odr_input")
            st_otr = request.POST.get("st_otr_input")
            
            # dobi ustrezno sobo z računom:
            for soba in podatki_za_racune:
                if int(soba["stsobe"])==int(st_sobe):
                    soba_za_racun = soba  # To je soba, ki sem jo dobil iz dicta podatki_za_racun, kjer so vse sobe z računi za ta dan
                    break
            # print(soba_za_racun["CENA"], st_odr, st_otr,
            #        soba_za_racun["st_noci"], soba_za_racun["StanjeTTAX"])
            
            preracunana_vrednost_nocitve, st_nocitev_nova, ttax_nov= data.preracunaj_vrednost_nocitve( 
                                                                            soba_za_racun["CENA"], 
                                                                            st_odr,
                                                                            st_otr,
                                                                            soba_za_racun["st_noci"],
                                                                            soba_za_racun["st_nocitev"],
                                                                            soba_za_racun["StanjeTTAX"]

                                                                            )
            
            
            # V dobljeni sobi_za_racun, ki gre v Json spremeni število odraslih, število otrok in ceno na nocitev
            soba_za_racun["SO"] = st_odr
            soba_za_racun["SOTR"] = st_otr
            soba_za_racun["cena_na_nocitev"] = preracunana_vrednost_nocitve
            soba_za_racun["st_nocitev"]= st_nocitev_nova
            soba_za_racun["TTAX"]= ttax_nov

            # V vnosGostov za to sobo vnesi cena_nocitve in stevilo_nocitev
            id_sobe_racun = soba_za_racun["id"]
            gost = VnosGostov.objects.get(id=id_sobe_racun)
            gost.nocitev_skupaj = st_nocitev_nova
            gost.st_noci = soba_za_racun["st_noci"]
            gost.cena_nocitve = soba_za_racun["cena_na_nocitev"]
            gost.SO = soba_za_racun["SO"]
            gost.SOTR = (soba_za_racun["SOTR"] if soba_za_racun["SOTR"] != "" else 0)
            gost.save()
            bar_narocila = (Bar_narocila.objects.select_related("gost").filter(gost=id_sobe_racun).
                         values('artikel_id', 'artikel__opis', 'artikel__cena', 'artikel__ddv', 'artikel__enota')
                        .annotate(kolicina_skupaj=Sum('kolicina')))

        # RAČUN
        elif "gumb_st_sobe" in request.POST:
            ob_datum_str= odpriJson(js_file=js_file)
            st_sobe = request.POST.get("gumb_st_sobe")  # Iz dicta dobi Value za Key="gumb_st_sobe"
            #print(st_sobe)
            for soba in podatki_za_racune:
                if int(soba["stsobe"])==int(st_sobe):
                    soba_za_racun = soba  # To je soba, ki sem jo dobil iz dicta podatki_za_racun, kjer so vse sobe z računi za ta dan
                    break

        
            # V vnosGostov za to sobo vnesi cena_nocitve in stevilo_nocitev
            id_sobe_racun = soba_za_racun["id"]
            gost = VnosGostov.objects.get(id=id_sobe_racun)
            gost.nocitev_skupaj = soba_za_racun["st_nocitev"]
            gost.cena_nocitve = soba_za_racun["cena_na_nocitev"]
            gost.st_noci = soba_za_racun["st_noci"]
            gost.save()

            # Pridobi bar naročila za to sobo
            bar_narocila = (Bar_narocila.objects.select_related("gost").filter(gost=id_sobe_racun).
                         values('artikel_id', 'artikel__opis', 'artikel__cena', 'artikel__ddv', 'artikel__enota')
                        .annotate(kolicina_skupaj=Sum('kolicina')))
        
        
        
        # shrani sobo za izdelavo računa v json
        js_file = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//racun_podatki.json')
    #    print(soba_za_racun)
        soba_za_racun["CENA"]=str(soba_za_racun["CENA"])
        soba_za_racun["ze_placano"]=str(soba_za_racun["ze_placano"])
        shraniJson(js_file=js_file, jsonData=soba_za_racun)
    
        context={"prihodi":prihodi, "odhodi":odhodi, 
                        "stayover":stayover, "menjave":menjave, 
                        "podatki_za_racun": soba_za_racun,
                        "forma": forma, "ob_datum": ob_datum_str,
                        "bar_narocila": bar_narocila}
    else: # GET
        # Shrani ob_datum v json. Začni z današnjim datumom, če se v datepickerju izbere drug datum se updata v jsonu 
        
        ob_datum = datetime.now().date()
        ob_datum_str = datetime.strftime(ob_datum, "%d.%m.%Y")
        ob_datum_json = ob_datum_str
        shraniJson(js_file=js_file, jsonData=ob_datum_json)
        
        ###____###
        data = Dn_izracuni(podatki=podatki, ob_datum= ob_datum)
        prihodi = data.prihodi()
        odhodi = data.odhodi()
        stayover = data.stayover()
        menjave = data.menjave()
        ###____###


        
        forma = Dn_form_izberi_datum() #initial={"moj_datum": date(2023, 5, 2) })#forma.fields["moj_datum"].widget.format = "%d.%m.%Y"
        
        context={"prihodi":prihodi, "odhodi":odhodi, 
                 "stayover":stayover, "menjave":menjave, 
                 "forma": forma, "ob_datum": ob_datum_str}
    return HttpResponse(template.render(context, request))



def tiskanje_racuna(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//racun_podatki.json')
    dict_podatki_za_tiskanje_racuna = odpriJson(js_file=js_file)
    
    id_soba_za_racun = dict_podatki_za_tiskanje_racuna["id"]
    ttax = dict_podatki_za_tiskanje_racuna["TTAX"]
    rna = dict_podatki_za_tiskanje_racuna["RNA"]
    
    gost = VnosGostov.objects.get(id=id_soba_za_racun)
    gost.status_placila = "placano_" + datetime.strftime(datetime.now().date(), "%d.%m.%y")
    gost.save()
    # OPCIJA, DA JE NA RAČUNU VSAK ARTIKEL VEČKRAT, 
    #gost_bar_narocila = Bar_narocila.objects.select_related("gost").filter(gost=id_soba_za_racun)
    
    # OPCIJA S SEŠTEVANJEM KOLIČIN ISTIH ARTIKLOV
    gost_bar_narocila = (Bar_narocila.objects.select_related("gost").filter(gost=id_soba_za_racun).
                         values('artikel_id', 'artikel__opis', 'artikel__cena', 'artikel__ddv', 'artikel__enota')
                        .annotate(kolicina_skupaj=Sum('kolicina')))
   
    podatki_tabela_za_racun = Tabela_za_racun(gost= gost, bar_narocila= gost_bar_narocila, ttax= ttax, rna= rna)
    tabela_za_racun, tabela_ddv, tabela_skupaj = podatki_tabela_za_racun.tabela_nocitev_bar()

    template = loader.get_template("form_dn_tiskanje_racuna.html")
    context= {"gost":gost, "gost_bar_narocila": gost_bar_narocila,
              "tabela": tabela_za_racun, "tabela_ddv": tabela_ddv, "tabela_skupaj": tabela_skupaj}  

    # Izbriši json s podatki za račun od prejšnje sobe:
    js_file_pocisti = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//racun_podatki.json')
    shraniJson(js_file=js_file_pocisti, jsonData={})

    return HttpResponse(template.render(context, request))













def tiskanje_multiracun(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//dn_ob_datum.json')
    ob_datum= odpriJson(js_file=js_file)
    ob_datum_dt = datetime.strptime(ob_datum, "%d.%m.%Y") 

    podatki_multiracun = Tebela_multiracun(ob_datum_dt= ob_datum_dt)
    dict_multiracunov = podatki_multiracun.priprava_podatkov()
    #print((dict_multiracunov))
    
    
    

    template= template = loader.get_template("form_dn_tiskanje_multiracun.html")   
    context={"dict_mr": dict_multiracunov,
             }

    return HttpResponse(template.render(context, request))


    #dict_podatki_za_tiskanje_racuna = odpriJson(js_file=js_file)






















def tiskanje_vingcard(request):
    js_file=js_file = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//dn_ob_datum.json')  
    ob_datum= odpriJson(js_file=js_file)
    ob_datum= datetime.strptime(ob_datum, "%d.%m.%Y")
    podatki = VnosGostov.objects.filter(status_rez="rezervirano")
    data = Dn_izracuni(podatki=podatki, ob_datum= ob_datum)
    prihodi = data.prihodi()
    template= loader.get_template("form_tiskanje_vingcard.html")
    context= {"prihodi": prihodi}

    return HttpResponse(template.render(context, request))
    
def tiskanje_porocilo(request):
    js_file=js_file = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//dn_ob_datum.json')  
    ob_datum= odpriJson(js_file=js_file)
    ob_datum= datetime.strptime(ob_datum, "%d.%m.%Y")
    podatki = VnosGostov.objects.filter(status_rez="rezervirano")
    data = Dn_izracuni(podatki=podatki, ob_datum= ob_datum)
    zajtrki = data.zajtrki_def()
    template= loader.get_template("form_tiskanje_porocilo.html")
    context= {"zajtrki": zajtrki,
              "ob_datum": ob_datum}

    return HttpResponse(template.render(context, request))

def siteminder(request):
    template = loader.get_template("form_siteminder.html")
    queryset = VnosGostov.objects.filter(status_rez="rezervirano")
    queryset_odpovedi = VnosGostov.objects.filter(status_rez="odpovedano")
    data = list(queryset.values())
    zadnji_vnos = queryset.latest("id")
    zadnja_odpoved = queryset_odpovedi.order_by("-datum_odpovedi_dt").first()
    
    od_datum = zadnji_vnos.od
    df_podatki = pd.DataFrame.from_records(data=data)
    

    if request.method=="POST":
        print(request.POST)
        od_dat_templ = request.POST.get("datum_template")
        if "od_zadnje_rez" in request.POST:
            od_datum = zadnji_vnos.od
        if "od_danes" in request.POST:
            od_datum = datetime.now().date().strftime("%d.%m.%Y")
        if "od_zadnje_odp" in request.POST:
            od_datum = zadnja_odpoved.od
        if "plus7" in request.POST:
            od_datum = datetime.strptime(od_dat_templ, "%d.%m.%Y") + timedelta(days=7)
            od_datum = datetime.strftime(od_datum, "%d.%m.%Y")
        if "minus7" in request.POST:
            od_datum = datetime.strptime(od_dat_templ, "%d.%m.%Y") - timedelta(days=7)
            od_datum = datetime.strftime(od_datum, "%d.%m.%Y")
        if "plus14" in request.POST:
            od_datum = datetime.strptime(od_dat_templ, "%d.%m.%Y") + timedelta(days=14)
            od_datum = datetime.strftime(od_datum, "%d.%m.%Y")
        if "minus14" in request.POST:
            od_datum = datetime.strptime(od_dat_templ, "%d.%m.%Y") - timedelta(days=14)
            od_datum = datetime.strftime(od_datum, "%d.%m.%Y")
        
        
            
        
        df_podatki_obdelani = Siteminder(podatki=df_podatki, od_datum=od_datum)
        podatki_sm = df_podatki_obdelani.obdelava_podatki_sm()
        context={"sm":podatki_sm, "od_datum": od_datum}
    else: # GET
    
        df_podatki_obdelani = Siteminder(podatki=df_podatki, od_datum=od_datum)
        podatki_sm = df_podatki_obdelani.obdelava_podatki_sm()
        context={"sm":podatki_sm, "od_datum": od_datum}



    return HttpResponse(template.render(context, request))


def grafikon(request):
    leto_primerjava = "2022"
    plot_image = Grafikoni().Pod_Kumulativa_DoDanes(leto_primerjava)              #Priprava_Podatkov(leto_primerjava="2022")
    template= loader.get_template("form_grafikoni.html")
    context = {
        'plot_image': plot_image,
        
    }
    return HttpResponse(template.render(context, request))
    """return render(request, 'chart_template.html', context)
    
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response"""

"""        
    template= loader.get_template("form_grafikoni.html")
    context={}

    return HttpResponse(template.render(context, request))
"""

"""
    # Pretvori string dat v dt_dat>> od c od_dt  ...
    #podatki = VnosGostov.objects.filter(status_rez="rezervirano")
    for d in podatki:
        if d.AvansEUR =="":
            d.AvansEUR = 0
        if d.SOMAL =="":
            d.SOMAL = 0
        if d.SOTR =="":
            d.SOTR = 0
        if d.dniPredr =="":
            d.dniPredr = 0
        
        datum_od= datetime.strptime(d.od,"%d.%m.%Y")
        d.od_dt = datum_od
        datum_do= datetime.strptime(d.do,"%d.%m.%Y")
        d.do_dt = datum_do
        datum_vnos= datetime.strptime(d.datumvnosa,"%d.%m.%Y")
        d.datumvnosa_dt = datum_vnos
        d.save()
    
    ####
    






#list_st_dictov = list(range(len(dict_multiracunov))) #!!!!! ustvari list iz range




def writetofile(request):
    f = open('C:/demo/test.txt', 'w')
    testfile = File(f)
    testfile.write('Welcome to this country')
    testfile.close
    f.close
    return HttpResponse()


def readfile(request):
    f = open("C:/Users/Hotel/Downloads/book.txt", "r", encoding='utf8')
    if f.mode == 'r':
        contents = f.read()
        print(contents)
    return HttpResponse()

"""




##################
"""
# CONVERT pandas df to queryset
from myapp.models import MyModel

# convert the DataFrame to a list of dictionaries
dicts = df.to_dict('records')

# create a list of MyModel objects from the list of dictionaries
instances = [MyModel(field1=d['column1'], field2=d['column2'], field3=d['column3']) for d in dicts]

# bulk create the MyModel objects to the database
MyModel.objects.bulk_create(instances)

# retrieve the newly created objects from the database as a queryset
queryset = MyModel.objects.filter(field1__in=[d['column1'] for d in dicts])


"""