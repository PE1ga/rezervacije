from typing import Any
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core import serializers

from django.urls import reverse

from django.conf import settings

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Aplikacija.models import Graf
from .models import *
import json
import os
import pandas as pd

# from datetime import datetime
import datetime as dt
from .forms import VnosRezForm, izborDatuma, izborProsteSobeVnos, SearchForm, IzborAgencije, IzborDatumovPonudba
from .definicije.razno import *
from .definicije.autofill import *
from .definicije.form_graf import *
from .definicije.iskanjeProstihSob import *
from .definicije.tabelaProsteSobe import *
from .definicije.ponudbaIzdelava import *
from .definicije.dashboard import *

"""def home_view(request):
    context ={}
    context['forma']= InputForm()
    return render(request, "formularTEST.html", context)"""


def form_home(request):
    gosti_seznam = VnosGostov.objects.all().values()
    # gosti_seznam = VnosGostov.objects.all().values()        #.order_by("-id").values()>> mi treba več -, ker je že definiran v models
    template = loader.get_template("form_home.html")
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


def form_Avtovnos(request):
    submitted = False  # Dokler ni gumb, form ni submt (Codemy.com)
    # Pridobi podatke o rez
    datumOD, datumDO = Autofill_def()
    if request.method == "POST":
        formular = izborProsteSobeVnos(request.POST)
        if formular.is_valid():
            tipS = formular.cleaned_data['tip']
            
            
            # queryset >> pandas
            queryset = VnosGostov.objects.all()
            data = list(queryset.values())
            df_data = pd.DataFrame.from_records(data=data)
            # queryset >> pandas
            queryset_sifrant = SifrantSob.objects.all()
            data = list(queryset_sifrant.values())
            df_sifrant_sob = pd.DataFrame.from_records(data=data)
            
            L_prosteSobe = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
            L_prosteSobeJson = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
            
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
            
            jsonData[0] = L_prosteSobeJson
            jsonData[3] = tipS

            shraniJson(js_file=js_file, jsonData=jsonData)
            
            ##############  END json ########

            # "/form_vnos_rocni")
            return HttpResponseRedirect("/form_vnos_izbor_sob/form_izberiSobo")
        else:
            print("Formular ni v celoti izpolnjen. Ni valid")

    else:  # GET __Form še ni bil (pravilno) izpolnjen
        formular = izborProsteSobeVnos(data={"od": datumOD, "do": datumDO})
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True

    context = {"forma": formular, "submitted": submitted,
               }

    # "form_vnos_rocni.html"
    return render(request, "form_predVnos.html", context)

    """
    
    cena, ime, agencija, stOseb, datumOD, datumDO, RNA, email, zahteve = Autofill_def()
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
    "do": datumDO, "RNA":RNA, "email": email, "zahteve": zahteve})
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True


    
    context ={"forma": formular, "submitted":submitted, }
    #"ImeStranke":"Jože Novak", "Agencija":agencija, "StOseb":stOseb, "DatumOD":datumOD,
    #"DatumDO": datumDO}
    
    return render(request, "form_Avtovnos.html", context)"""


def form_vnos_rocni(request):

    submitted = False  # Dokler ni gumb, form ni submt (Codemy.com)
    # Pridobi podatke od JSONA
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    
    jsonData = odpriJson(js_file=js_file)
    

    #  0: Razpoložljive sobe,
#  1: Od  2: Do  3: Tip 4: Ime
#  5: Št oseb 6: Št Sobe 7: Cena
#  8: Agencija 9: Država 10: RNA
#  11: Zahteve 12: email
    od = jsonData[1]
    do = jsonData[2]
    tip = jsonData[3]
    StSobe = jsonData[6]
    ime = jsonData[4]
    CENA = jsonData[7]
    agencija = jsonData[8]
    RNA = jsonData[10]
    zahteve = jsonData[11]
    email = jsonData[12]
    datumvnosa = pd.to_datetime("today").strftime(format="%d.%m.%Y")
    if agencija == "Siteminder" or agencija == "Cesta" or agencija == "Nasi":
        stanjeTtax = "Ttax JE VKLJ"
    elif agencija == "":
        stanjeTtax = ""
    else:
        stanjeTtax = "Ttax NI VKLJ"

    if request.method == "POST":
        formular = VnosRezForm(request.POST)
        if (request.POST['dniPredr'] == ''):

            dniPredr = 0
        if formular.is_valid():
            formular.save()
            formular = VnosRezForm()

            return HttpResponseRedirect("/form_vnos_rocni?submitted=True")
        else:
            print("Formular ni v celoti izpolnjen. Ni valid")

    else:  # GET __Form še ni bil (pravilno) izpolnjen
        if jsonData[0] != "0":
            formular = VnosRezForm(data={"datumvnosa": datumvnosa, "od": od, "do": do, "tip": tip, "stsobe": StSobe,
                                         "imestranke": ime, "CENA": CENA, "agencija": agencija, "RNA": RNA,
                                         "zahteve": zahteve, "email": email, "StanjeTTAX": stanjeTtax})

        # Resetiraj JsonFile
        jsonData = [[], "", "", "", "", "", "", "", "", "", "", "", "",]
        shraniJson(js_file=js_file, jsonData=jsonData)
        
        if "submitted" in request.GET:  # Ali je bil form že submitan?
            submitted = True

    context = {"forma": formular, "submitted": submitted, }

    return render(request, "form_vnos_rocni.html", context)


def form_vnos_izbor_sob(request):  # TO BO PRVA FAZA ROČNEGA VNOSA!!!!
    submitted = False  # Dokler ni gumb, form ni submt (Codemy.com)
    if request.method == "POST":
        formular = izborProsteSobeVnos(request.POST)
        # formular = VnosRezForm(data={"imestranke":"Peter","agencija":"Nasi"})
        if formular.is_valid():
            datumOD = formular.cleaned_data['od']
            datumDO = formular.cleaned_data['do']

            tipS = formular.cleaned_data['tip']

            
            # queryset >> pandas
            queryset = VnosGostov.objects.all()
            data = list(queryset.values())
            df_data = pd.DataFrame.from_records(data=data)
            # queryset >> pandas
            queryset_sifrant = SifrantSob.objects.all()
            data = list(queryset_sifrant.values())
            df_sifrant_sob = pd.DataFrame.from_records(data=data)
            
            
            L_prosteSobe = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
            L_prosteSobeJson = proste_sobe(df_data, df_sifrant_sob, tipS, datumOD, datumDO)
           # datumOD = datumOD.strftime("%d.%m.%Y")
           # datumDO = datumDO.strftime("%d.%m.%Y")

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
            
            jsonData[0] = L_prosteSobeJson
            jsonData[1] = datumOD
            jsonData[2] = datumDO
            jsonData[3] = tipS
            jsonData[4] = ""
            jsonData[5] = ""
            jsonData[6] = ""
            jsonData[7] = ""
            jsonData[8] = ""
            jsonData[9] = ""
            jsonData[10] = ""
            jsonData[11] = ""
            jsonData[12] = ""

            shraniJson(js_file=js_file, jsonData=jsonData)
            
            ##############  END json ########

            # "/form_vnos_rocni")
            return HttpResponseRedirect("/form_vnos_izbor_sob/form_izberiSobo")
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


#  0: Razpoložljive sobe,
#  1: Od  2: Do  3: Tip4: Ime
#  5: Št oseb 6: Št Sobe 7: Cena
#  8: Agencija 9: Država 10: RNA
#  11: Zahteve 12: email


def form_izberi_sobo(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    jsonData = odpriJson(js_file=js_file)
    listRazpolozljSob = jsonData[0]

    """tuppleSob = []
    for i in listSob:
        tuppleSob.append((str(i),str(i)))"""

    if request.method == "POST":
        # formular = IzberiSobo(request.POST)
        # if formular.is_valid():
        # formular.cleaned_data['izberisobo']
        IzbranaSoba = request.POST.get("izberisobo")
        # print(IzbranaSoba)
        jsonData[6] = IzbranaSoba

        shraniJson(js_file=js_file, jsonData=jsonData)
       
            # formular = IzberiSobo()

        return HttpResponseRedirect("/form_vnos_rocni")
        # else:
        #   print("Formular ni v celoti izpolnjen. Ni valid")

    # else:  # GET __Form še ni bil (pravilno) izpolnjen
        # formular = IzberiSobo.fields['izberisobo'].choices = tuppleSob
    #    formular = IzberiSobo() #data={ 'izberisobo': tuppleSob })

    # context ={"forma": formular, "choices": listRazpolozljSob }
    context = {"choices": listRazpolozljSob}

    return render(request, "form_izberiSobo.html", context)


def updateIzSeznama(request, id):

    gost = VnosGostov.objects.get(id=id)
    obDatum = gost.od
    tipSobe = gost.tip
    listSob = seznamSob(tipSobe)
    
    # queryset >> pandas
    queryset = VnosGostov.objects.all()
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
            return HttpResponseRedirect("/form_home")
        else:
            print("Form ni VALID")
    else:  # GET
        form = VnosRezForm(instance=gost)

    context = {"rezervacije": rezervacije,
               "forma": form, "gost": gost, "listSob": listSob}
    return HttpResponse(template.render(context, request))


def delete_gost(request, id):
    gost = VnosGostov.objects.get(id=id)
    template = loader.get_template("form_delete.html")
    if request.method == "POST":
        gost.delete()
        return HttpResponseRedirect("/form_home")

    context = {"item": gost}
    return HttpResponse(template.render(context, request))


def form_graf(request):
    # pridobi podatke iz arhiva rezervacij
    # sosed FORM_GRAF.py  #"R_Optimi"))   "DN")) R_Optimi_iskanjeRez
    

    # Briši vse instance v database Graf
    Graf.objects.all().delete()
    # queryset >> pandas
    queryset = VnosGostov.objects.all()
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    df_graf= IzdelavaGrafa(df_data, pd.to_datetime("today"), "R_Optimi")
    # Pretvori Padas >> Queryset
    my_dict = df_graf.to_dict(orient="records")
    my_instances = [Graf(**d) for d in my_dict]
    Graf.objects.bulk_create(my_instances)




    if request.method == "POST":
        formular = izborDatuma(request.POST)
        if formular.is_valid():
            # cleaned_data da dobiš vrednost forma po submitu v views.py
            datum = formular.cleaned_data['datum']
            tipSobe = formular.cleaned_data['tipSobe']
            
            # Briši vse instance v database Graf
            Graf.objects.all().delete()
            # queryset >> pandas
            queryset = VnosGostov.objects.all()
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
            #rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
            #                                  "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
            #                                  "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")

            context = {"rezervacije": rezervacije,
                       "formDatum": formular, "listSob": listSob}
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
                   "formDatum": formular, "listSob": listSob}
        template = loader.get_template("form_graf.html")

        return HttpResponse(template.render(context, request))

"""
def updateIzGrafa(request, komande):
    id = int(komande.split(sep="_")[0])
    gost = VnosGostov.objects.get(id=id)
    template = loader.get_template("form_update.html")
    form = VnosRezForm(request.POST, instance=gost)
    datumOD = gost.od
    rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                      "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                      "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")

    if request.method == 'POST':
        if form.is_valid():
            # update the existing `Band` in the database
            form.save()
            # redirect to the detail page of the `Band` we just updated
            # return HttpResponseRedirect(template, gost.id)
            return HttpResponseRedirect("/form_graf")
        else:
            context = {"forma": form, "gost": gost, "rezervacije": rezervacije}

            print("Form ni VALID")

    else:  # GET
        form = VnosRezForm(instance=gost)
        tipSobe = gost.tip
        listSob = seznamSob(tipSobe)
        
        # queryset >> pandas
        queryset = VnosGostov.objects.all()
        data = list(queryset.values())
        df_data = pd.DataFrame.from_records(data=data)
        
        IzdelavaGrafa(df_data, pd.to_datetime(datumOD, format="%d.%m.%Y"), "R_Optimi")
        rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                          "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                          "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")

        context = {"forma": form, "gost": gost,
                   "rezervacije": rezervacije, "listSob": listSob}

    return HttpResponse(template.render(context, request))
"""

def updateIzGrafa2(request, komande):
    print(request.method)
    # print(request.POST)
    if isinstance(komande, int):
        id = komande
    else:
        razclemba = komande.split(sep="_")
        id = int(razclemba[0])

    gost = VnosGostov.objects.get(id=id)
    tipSobe = gost.tip
    datumOD = gost.od
    stSobe = gost.stsobe
    
    

    """# Briši vse instance v database Graf
    Graf.objects.all().delete()
    # queryset >> pandas
    queryset = VnosGostov.objects.all()
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    df_graf= IzdelavaGrafa(df_data, pd.to_datetime(datumOD, format=("%d.%m.%Y")), "R_Optimi")
    # Pretvori Padas >> Queryset
    my_dict = df_graf.to_dict(orient="records")
    my_instances = [Graf(**d) for d in my_dict]
    Graf.objects.bulk_create(my_instances)

    
    form = VnosRezForm(request.POST, instance=gost)
    template = loader.get_template("form_update.html")"""
    rezervacije = Graf.objects.values("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7",
                                      "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17",
                                      "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26", "S27", "S28")
    template = loader.get_template("form_update.html")
    form = VnosRezForm(request.POST, instance=gost)
    
    if request.method == 'POST':
        if form.is_valid():

            # Izbris sobe

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
            queryset = VnosGostov.objects.all()
            data = list(queryset.values())
            df_data = pd.DataFrame.from_records(data=data)
            # queryset >> pandas  ŠIFRANT SOB
            queryset_sifrant = SifrantSob.objects.all()
            data = list(queryset_sifrant.values())
            df_sifrant_sob = pd.DataFrame.from_records(data=data)
            
            L_prosteSobe = proste_sobe(df_data, df_sifrant_sob, TipSobeForm, DatumODform, DatumDOform)
            print(L_prosteSobe)
            # Prestavi sobo v drugo sobo
            if StSobeForm in L_prosteSobe or StSobeForm == stSobe:  # or TipSobeForm == tipSobe:
                # S formom je vse ok, shrani ga
                form.save()
                # Briši vse instance v GRAF
                Graf.objects.all().delete()
                # queryset >> pandas  ARHIV GOSTOV
                queryset = VnosGostov.objects.all()
                data = list(queryset.values())
                df_data = pd.DataFrame.from_records(data=data)
                
                df_graf=IzdelavaGrafa(df_data, pd.to_datetime(datumOD, format="%d.%m.%Y"), "R_Optimi")
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
        queryset = VnosGostov.objects.all()
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
                   "listSob": listSob, "IzbrTipSobe": tipSobe}

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

            virtualRez = VnosGostov.objects.filter(
                RNA="ExpColl", agencija=vrstaAgencije)
            virtualRez = sorted(virtualRez, key=lambda obj: dt.datetime.strptime(
                obj.od, "%d.%m.%Y"), reverse=False)
            template = loader.get_template("form_virtual.html")
            context = {"virtualRez": virtualRez, "forma": form}

            return HttpResponse(template.render(context, request))

    else:  # GET
        jsonData = odpriJson(js_file=js_file)  # Sosed: Razno.py
        vrstaAgencije = jsonData[0]
        form = IzborAgencije(data={"vrstaAgencije": vrstaAgencije})
        # Sorting Sortiranje in pretvarjanje datuma iz string v datetime.datetime.strptime
        virtualRez = VnosGostov.objects.filter(
            RNA="ExpColl", agencija=vrstaAgencije)
        virtualRez = sorted(virtualRez, key=lambda obj: dt.datetime.strptime(
            obj.od, "%d.%m.%Y"), reverse=False)
        template = loader.get_template("form_virtual.html")
        context = {"virtualRez": virtualRez, "forma": form}
        return HttpResponse(template.render(context, request))


def virtual_podrobno(request, id):
    record = VnosGostov.objects.get(id=id)
    template = loader.get_template('form_virt_podrobno.html')
    context = {"rezervacija": record}

    return HttpResponse(template.render(context, request))


def virtual_spremeni_status(request, id):
    record = VnosGostov.objects.get(id=id)
    if record.AvansEUR == "":
        record.AvansEUR = None
    if record.IDponudbe == "":
        record.IDponudbe = None

    record.RNA = "NONREFOK"
    record.save()

    return HttpResponseRedirect("/form_virtual")


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
                                 'ime': ime, 'email': email, 'rna': rna, 'avans': avans, 'odpoved': odpoved}
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
    
    
     # queryset >> pandas  ARHIV GOSTOV
    queryset = VnosGostov.objects.all()
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    # queryset >> pandas  ŠIFRANT SOB
    queryset_sifrant = SifrantSob.objects.all()
    data = list(queryset_sifrant.values())
    df_sifrant_sob = pd.DataFrame.from_records(data=data)
    
    
    
    
    dictProstihSob = prosteSobeZaPonudbo(df_data, df_sifrant_sob, odDatum=odDatum, doDatum=doDatum)
    template = loader.get_template("form_ponudba_faza_2.html")
    context = {"dictProstihSob": dictProstihSob, "dictVhodovPonudba": dictVhodovPonudba}
    return HttpResponse(template.render(context, request))


# def brez templata >> samo pobere podatke iz tabele in jih vnese v Json
def ponudba_tip_sobe(request, tip) -> HttpResponseRedirect:
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
    # return HttpResponse(template.render(context, request))


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
        stSobVprvemTipSobe = dictVhodovPonudba["tipSobe"][0][3]
        vrstaInAli = dictVhodovPonudba["vrstaInAli"]
        # print(L_steviloSob)
        # ugotovi MR:
        if (L_steviloSob > 1 or int(stSobVprvemTipSobe) > 1) and vrstaInAli == "IN":
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
                             status="0_Vnesena",
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

    # Vzorec instance
    # person = Person(name=my_data['name'], age=my_data['age'], email=my_data['email'])
    # person.save()


def ponudba_predogled(request):
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')
    dictVhodovPonudba = odpriJson(js_file=js_file)  # Sosed: Razno.py
    htmlTekst= ponudbaHtml(dictPonudba=dictVhodovPonudba)
    context= {"htmlTekst": htmlTekst, 'api_key': 'ks18lj2k2vyzd0lh6rf7j45pvl62hj3b45xibxvq5b985n81'}
    template = loader.get_template("form_ponudba_predogled.html")
    return HttpResponse(template.render(context, request))



def ponudba_poslji(request):
    modificiran_html = request.POST.get("html_text")
    email = EmailMessage(subject="Ponudba ", body= modificiran_html, from_email= "peter.gasperin57@gmail.com", to= ["peter.gasperin@siol.net",]
                    )
    # Set the HTML version of the message
    email.content_subtype = 'html'
    email.body = modificiran_html
    
    email.send()
    return HttpResponseRedirect("/form_ponudba_predogled")



def ponudba_brisi_sobo(request, id_sobe):
    print(id_sobe-1)
    js_file = os.path.join(
        settings.BASE_DIR, 'Rezervacije//static//json//ponudbaVhod.json')
    dictVhodovPonudba = odpriJson(js_file=js_file)  # Sosed: Razno.py
    del dictVhodovPonudba["tipSobe"][id_sobe-1]
    shraniJson(js_file=js_file, jsonData=dictVhodovPonudba)  # Sosed: Razno.py

    return HttpResponseRedirect("/form_ponudba_faza_1/form_ponudba_faza_2")



def ponudba_seznam(request):
    ponudbe = Ponudba.objects.all().values()
    context={"ponudbe": ponudbe}
    template=loader.get_template("form_ponudba_seznam.html")
    
    return HttpResponse(template.render(context,request))


def ponudba_obdelava(request, id):
    ponudba = Ponudba.objects.get(id=id)
    print(ponudba)
    context= {"ponudba": ponudba}
    template = loader.get_template("form_ponudba_obdelava.html")

    return HttpResponse(template.render(context,request))










def dashboard(request):
    template = loader.get_template("form_dashboard.html")
    # Zberi podatke iz Vnos-a kot QS, in jih pretvori v DF, ki ga pošlješ k sosedu dashboard.py >> querset to pandas
    queryset = VnosGostov.objects.all()
    data = list(queryset.values())
    df_data = pd.DataFrame.from_records(data=data)
    
    df_podatki= rezultati_po_mescih(df_data,"2022")
    
    
    context={"df_nocitve":df_podatki}
    return HttpResponse(template.render(context, request))









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