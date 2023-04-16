from django import forms
#from bootstrap_datepicker_plus import DatePickerInput
from django.forms import ModelForm, Select, TextInput, DateInput 
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.conf import settings 



from .models import VnosGostov, Ponudba
import json
import os  
import datetime as dt

class izborDatuma(forms.Form): # ZA GRAF
    datum = forms.DateField( required=True,
        label="Vnesi Datum", 
        widget=forms.DateInput(format='%d.%m.%Y', 
            attrs={"class":"form-control", "style":"font-size:14px;width:auto; height:auto"}),
            input_formats=['%d.%m.%Y'])
    
    tipSobe = forms.CharField(required=False,
        label="Tip Sobe",

        max_length= 10,
        widget=forms.Select( choices=[("vse","vse"),("c","c"),("g","g"),("s","s"),("f","f"),("x","x"),
                ("y","y"),("q","q"),("d","d"),], 
                attrs={"class":"form-control","style":"font-size:14px; width:auto; height:auto"})
        )
         

class IzborAgencije(forms.Form):  # za Virtual >> Izbere UNIKATNE vrednosti agencij !!!!!
    unikatneVrednosti= VnosGostov.objects.filter(RNA="ExpColl", status_rez="rezervirano").order_by("agencija").values_list("agencija", flat=True).distinct()
    CHOICES= [(value, str(value)) for value in unikatneVrednosti]   # Izdela LIST CHOICESOV ZA ChoiceField !!!!!
    
    vrstaAgencije = forms.ChoiceField(choices=CHOICES, label="Izberi Agencijo")
    

class izborSobeVnos(forms.Form):
    tipSobe = forms.CharField(
        label="Tip Sobe",
        max_length= 10,
        widget=forms.Select(choices=[("",""),("c","c"),("g","g"),("s","s"),("f","f"),("x","x"),("y","y"),("q","q"),("d","d"),])
        )
    


class izborProsteSobeVnos(forms.Form):  # ZA AUTOVNOS - predvnos _1.faza
    od = forms.CharField(label="Vnesi datum OD", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    do = forms.CharField(label="Vnesi datum DO", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tip = forms.CharField(
        label="Tip Sobe",
        max_length= 10,
        widget=forms.Select(choices=[("",""),("c","c"),("g","g"),("s","s"),("f","f"),("x","x"),("y","y"),("q","q"),("d","d"),], attrs={'class':'form-control'})
        )
class IzberiSoboVnos(forms.Form):
    izberisobo = forms.ChoiceField()
    
    """
    prosteSobe = forms.CharField(
        label="Razpoložljive sobe",
        max_length= 10,
        widget=forms.Select(choices=[("",""),("c","c"),("g","g"),("s","s"),("f","f"),("x","x"),("y","y"),("q","q"),("d","d"),])
        ) """




class SearchForm(forms.Form):
    search_field = forms.CharField(max_length=100, required=False)


class Gumbi(forms.Form):
    id_gumba = forms.CharField(max_length=10, show_hidden_initial=True)


class VnosRezForm(forms.ModelForm):
    #JS_file = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
    #with open(JS_file, "r", encoding="utf-8") as f:
    #    jsonData = json.load(f)
    status_rez = forms.CharField(label="Status", max_length=50, initial="rezervirano",  widget=forms.TextInput(attrs={'class': 'form-control'}))
    od = forms.CharField(label="Datum OD", max_length=50, error_messages={"required":"Manjka Podatek"}, widget=forms.TextInput(attrs={'class': 'form-control'}))
    do = forms.CharField(label="Datum DO",max_length=50, error_messages={"required":"Manjka Podatek"}, widget=forms.TextInput(attrs={'class': 'form-control'}))
    stsobe = forms.IntegerField(label="Št. Sobe", error_messages={"required":"Manjka vnos"}, widget=forms.TextInput(attrs={'class': 'form-control'}))
    imestranke = forms.CharField(label="Ime", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    CENA = forms.CharField(label="Cena", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dniPredr = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    AvansEUR = forms.CharField(label="Avans", required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    zahteve = forms.CharField(label="Zahteve", required=False, max_length=255,widget=forms.Textarea(attrs={'class':'form-control', 'style':'height:100px;'}))
    Alergije = forms.CharField(label="Alergije", required=False, max_length=255,widget=forms.Textarea(attrs={'class':'form-control', 'style':'height:30px;'}))
    SOTR= forms.CharField(label="Št. Otrok", required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    SOMAL= forms.CharField(label="Št. Malčkov",required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    datumvnosa = forms.CharField(label="Datum Vnosa", required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    SO = forms.CharField(label="Št. Oseb", max_length=20, widget=Select(choices=[("",""),(1,1),(2,2),(3,3),(4,4),(5,5)], attrs={'class': 'form-control',"style":""}))
    Zaklenjena = forms.CharField(label="Zaklenjena D/N", required=False, max_length=50, widget=Select(choices={("",""), ("Zaklenjena","Zaklenjena")}, attrs={'class': 'form-control'}))
    DR= forms.CharField(label="Država", max_length=100, widget= Select(choices=[("",""),
                ("??","??"),("SI","SI"),("AT","AT"),("AU","AU"),("BA","BA"),("BE","BE"),("BR","BR"),("BY","BY"),("CA","CA"),
                ("CH","CH"),("CN","CN"),("CZ","CZ"),("DE","DE"),("DK","DK"),("ES","ES"),("FI","FI"),("FR","FR"),("GB","GB"),
                ("HK","HK"),("HR","HR"),("HU","HU"),("IE","IE"),("IL","IL"),("IN","IN"),("IS","IS"),("IT","IT"),("KR","KR"),
                ("LT","LT"),("NL","NL"),("NO","NO"),("MT","MT"),("PL","PL"),("PT","PT"),("RO","RO"),("RU","RU"),("RS","RS"),
                ("SE","SE"),("SG","SG"),("SK","SK"),("TW","TW"),("UA","UA"),("US","US")], 
                attrs={'class': 'form-control',"style":""}))
    #IDPonudbe= forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'})) 


    def clean_CENA(self):
        decimal = self.cleaned_data['CENA']
        if "," in str(decimal):
            raise ValidationError("Vnesti moraš ceno s . in ne , !")
        return decimal
    
    
    # S temi kodami preprečiš, da form ne zahteva števila v integer fieldih
    def clean_dniPredr(self):
        dniPredr = self.cleaned_data.get('dniPredr')
        if not dniPredr:
            return None
        return dniPredr
    
    def clean_AvansEUR(self):
        AvansEUR = self.cleaned_data.get('AvansEUR')
        if not AvansEUR:
            return None
        return AvansEUR
    
    def clean_SOTR(self):
        SOTR = self.cleaned_data.get('SOTR')
        if not SOTR:
            return None
        return SOTR  
    
    def clean_SOMAL(self):
        SOMAL = self.cleaned_data.get('SOMAL')
        if not SOMAL:
            return None
        return SOMAL
    
    def clean_IDponudbe(self):
        IDponudbe = self.cleaned_data.get('IDponudbe')
        if not IDponudbe:
            return None
        return IDponudbe


    class Meta():
        model = VnosGostov
        exclude = []
        #fields ="__all__"
        
        widgets = {
            #'od': forms.widgets.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'class': 'form-control'}),
            #'do': forms.widgets.DateInput(format='%d.%m.%Y', attrs={'type': 'text', 'class': 'form-control'}),
            "tip": Select(choices=[("",""),("c","c"),("g","g"),("s","s"),("f","f"),("x","x"),("y","y"),("q","q"),("d","d"),], attrs={'class': 'form-control',"style":""}),
            "agencija": Select(attrs={'class': 'form-control',"style":"; " }, choices=[("",""),("Nasi","Nasi"),("Siteminder","Siteminder"),("Booking.com","Booking.com"),("Expedia","Expedia"),("Agoda","Agoda"),("HotelBEDS","HotelBEDS"),("Cesta","Cesta"),("Vrh","Vrh"),("LTO","LTO"),("TuristBiro","TuristBiro")]),
            "email": forms.EmailInput(attrs={"input_type" :'email', "placeholder": "@","style":"", "class": "form-control" }),
            "StanjeTTAX": Select(choices=[("",""),("Ttax JE VKLJ","Ttax JE VKLJ"),("Ttax NI VKLJ","Ttax NI VKLJ")],  attrs={'class': 'form-control',"style":""}),
            "RNA": Select(choices=[("",""),("ref","ref"),("refOK","refOK"),("ExpColl","ExpColl"),("Nonref","Nonref"),("NONREFOK","NONREFOK"),("Virtual","Virtual"),("Avans","Avans"),("AVANSOK","AVANSOK")], attrs={'class': 'form-control',"style":""}), 
            
            }
        
        
        fields =[ 
        
                	
                "imestranke",	
                "agencija",	
                "tip",	
                "od", 
                "do", 
                "dniPredr",
                "CENA", 
                "stsobe",
                "SO",	
                "RNA",
                "AvansEUR",
                "email",
                "DR",	
                "Alergije",
                #"Mes_Let",	
                #"Noc_SK", 
                "StanjeTTAX",
                #"OdpRok", 
                #"IDponudbe",
                #"RokPlacilaAvansa",
                "Zaklenjena",
                #"OdpovedDne",
                "SOTR",
                "SOMAL",
                "datumvnosa",
                "zahteve",
                "status_rez",

                ]
   


class IzborDatumovPonudba(forms.Form):  # PONUDBA - 1. FAZA
    od = forms.CharField(label="OD", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    do = forms.CharField(label="DO", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ime = forms.CharField(label="Ime", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    jezik = forms.CharField(error_messages={'required':'Izberi jezik'}, label="Jezik", max_length=100, widget=forms.Select(choices=[("",""),("SLO","SLO"),("GB","GB")], attrs={'class': 'form-control'})) 
    vrstaInAli = forms.CharField(label="In Ali", max_length=100, widget=forms.Select(choices=[("",""),("IN","IN"),("ALI","ALI")], attrs={'class': 'form-control'})) 
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    rna = forms.CharField(label="Tip rezerv.", widget=forms.Select(choices=[("",""),("Avans","Avans"),("Nonref","Nonref"),("CCD","CCD"),("Brez","Brez")],attrs={'class': 'form-control'}))
    avans = forms.IntegerField(required=False , widget=forms.TextInput(attrs={'class': 'form-control'}))
    odpoved = forms.IntegerField(label="Odp. rok",widget=forms.Select(choices=[("",""),("2","2"),("7","7"),("14","14")],attrs={'class': 'form-control'}))





class PonudbaForm(forms.ModelForm):
    id = forms.IntegerField()
    datumVnosa= forms.CharField(max_length=30) 
    status = forms.CharField(max_length=30, widget=forms.Select(choices=[("0_Nepotrjeno", "0_Nepotrjeno"), ("1_Poslano", "1_Poslano")], attrs={"class":"form-control"})) 
    ime = forms.CharField(max_length=30) 
    od = forms.CharField(max_length=30) 
    do = forms.CharField(max_length=30) 
    email = forms.CharField(max_length=30) 
    rna = forms.CharField(max_length=30) 
    avans = forms.IntegerField(required=False)
    odpoved = forms.IntegerField()
    stOdr = forms.IntegerField()
    stOtr = forms.CharField(max_length=30, required=False) 
    tip = forms.CharField(max_length=30) 
    cena = forms.IntegerField()
    odpRok= forms.CharField(max_length=30, required=False)
    jezik= forms.CharField(max_length=30)
    multiroom= forms.CharField(max_length=30, required=False)
    datumPotrditve= forms.CharField(max_length=30, required=False)
    sklic= forms.CharField(max_length=30, required=False)
    zahteve= forms.CharField(max_length=255, required=False)
    stNocitev= forms.CharField(max_length=30, required=False)
    dodatnoLezisce= forms.CharField(max_length=30, required=False)
    rokPlacilaAvansa= forms.CharField(max_length=30, required=False)
    skiXXdn= forms.CharField(max_length=30, required=False)
    skiOsebe= forms.CharField(max_length=30, required=False)
    skiCenaSkiInNast= forms.CharField(max_length=30, required=False)

    class Meta():
        model = Ponudba
        exclude = []
        fields =[          #"__all__"
                "id", 
                "ime",
                "datumVnosa",
                "status",
                "email",
                "od",
                "do",
                "rna",
                "avans",
                "odpoved",
                "stOdr",
                "stOtr",
                "tip",
                "cena",
                "odpRok",
                "jezik",
                "multiroom",
                "datumPotrditve",
                "sklic",
                "zahteve",
                "stNocitev",
                "dodatnoLezisce",
                "rokPlacilaAvansa",
                "skiXXdn",
                "skiOsebe",
                "skiCenaSkiInNast"
                ]


"""class Bar_form(forms.Form):
    danes = dt.date.today()      #.strftime("%d.%m.%Y")
    qs_stayover= VnosGostov.objects.filter(Q(od_dt__lte=danes) & Q(do_dt__gt=danes)).order_by("stsobe")
    list_stayover_st_sob=[]
    list_stayover_id_rez=[]
    for dict in qs_stayover:
        list_stayover_st_sob.append(dict.stsobe) # tuple (id, št.sobe) >> id je value, ki ga v view rabiš za obdelavo, št sobe je
    for dict in qs_stayover:
        list_stayover_id_rez.append(dict.id)

    choices = []
    for choice in range(len(list_stayover_id_rez)):
        tuple_choice = list_stayover_id_rez[choice], list_stayover_st_sob[choice]
        choices.append(tuple_choice)

    #print(list_stayover)
    list_sob_choice = [(value, value) for value in list_stayover_st_sob]

    soba = forms.CharField(max_length=30, widget=forms.Select(choices=choices, 
                                                              attrs={"class":"form-control"})) """


class Bar_form(forms.Form):
    """In this example, we move the code that generates the choices list into the __init__() 
    method of the form. 
    This means that the choices list will be regenerated each time the form is instantiated, 
    and any new records added to the VnosGostov model will be included in the choices list.

    Note that we also update the widget attribute of the soba field to include the choices list, 
    rather than passing it as an argument to the Select widget."""
    soba = forms.CharField(max_length=30, widget=forms.Select(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        danes = dt.date.today()
        qs_stayover= VnosGostov.objects.filter(status_rez = "rezervirano")
        qs_stayover= qs_stayover.filter(Q(od_dt__lte=danes) & Q(do_dt__gt=danes)).order_by("stsobe")
        list_stayover_st_sob=[]
        list_stayover_id_rez=[]
        for dict in qs_stayover:
            list_stayover_st_sob.append(f"{dict.stsobe} - {dict.imestranke}")
        for dict in qs_stayover:
            list_stayover_id_rez.append(dict.id)

        choices = []
        for choice in range(len(list_stayover_id_rez)):
            tuple_choice = list_stayover_id_rez[choice], list_stayover_st_sob[choice]
            choices.append(tuple_choice)
        tuple_0 = ("","")
        choices.insert(0,tuple_0)


        self.fields['soba'].widget.choices = choices




class Dn_form_izberi_datum(forms.Form):
    moj_datum = forms.DateField(widget=DateInput(attrs={'type': 'date', "class":"form-control"}, format=['%d.%m.%Y']), input_formats=['%d.%m.%Y'])  #forms.DateInput(format="%d.%m.%Y"))













"""
# creating a form Codemy
class UpdateRezForm(ModelForm):
    class Meta():
        model = VnosGostov
        exclude = []
        fields ="__all__"
"""
    
    
    
    
    
"""
    
    FRUIT_CHOICES= [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
    ]
class InputForm(forms.Form):
    first_name= forms.CharField(max_length=100)
    last_name= forms.CharField(max_length=100)
    email= forms.EmailField()
    age= forms.IntegerField()
    favorite_fruit= forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))


class NameForm(forms.Form): # Django tutor
    your_name = forms.CharField(label='Your name', max_length=100)


    
    
    
    
    
    
    
    
    od =forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=['%d.%m.%Y'])
    do = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=['%d.%m.%Y'])
    RokPlacilaAvansa  = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y', attrs={
                'type': 'date', 
                'class': 'form_input',}),
        input_formats=['%d.%m.%Y'])
    OdpovedDne = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=['%d.%m.%Y'])"""
    
    
    
"""class Meta:
        model = VnosGostov
        #fields = "__all__"    #["Soba","Akcija", "Agencija"]
        fields =[ 
        
                "sifravnosa",	
                "imestranke",	
                "agencija",	
                "od", 
                "do", 
                "dniPredr",
                "CENA", 
                "stsobe",
                "SO",	
                "tip",	
                "RNA",
                "AvansEUR",
                "email",
                "DR",	
                "zahteve",
                "Alergije",
                "Mes_Let",	
                "Noc_SK", 
                "StanjeTTAX",
                "OdpRok", 
                "IDponudbe",
                "RokPlacilaAvansa",
                "Zaklenjena",
                "OdpovedDne",
                "SOTR",
                "SOMAL"]
                        
      
        
        widgets = {
        "stsobe": Select(choices=[(0,0),(10,10),(20,20)]), 
        "SO":Select(choices=[(1,1),(2,2)]), 
        "agencija": Select(choices=[("",""),("Nasi","Nasi"),("Siteminder","Siteminder"),("Booking.com","Booking.com"),("Expedia","Expedia"),("Agoda","Agoda"),("HotelBEDS","HotelBEDS"),("Cesta","Cesta"),("Vrh","Vrh"),("LTO","LTO"),("TuristBiro","TuristBiro")]),
        "email": forms.EmailInput(attrs={"input_type" :'email', "placeholder": "@","style":"background-color:red;" }),
        
        }
         
            "od": forms.DateInput(
            format= ('%d-%m-%Y'), 
            attrs={'class': 'form-control form-control-sm', 
               'placeholder': 'Select a date',
               'type': 'date'
              }),"""
        
        



