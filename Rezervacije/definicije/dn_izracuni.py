
from django.db.models import Q, F
from datetime import timedelta



class Dn_izracuni:
    def __init__(self, podatki , ob_datum):
        self.podatki = podatki
        self.ob_datum = ob_datum
        #print(podatki)
    
    def prihodi(self):
        self.prihodi_data = self.podatki.filter(od_dt=self.ob_datum)

        # dodaj stevilo noci (rabiš za vingcard)
        for prihod in self.prihodi_data:
            st_noci = prihod.do_dt - prihod.od_dt 
            st_noci= st_noci.days
            prihod.st_noci = st_noci
            prihod.save()
        
            # v polje se_placati dodaj znesek, ki naj se vstavi v vingcard  ## PAZI!! UPORABIL NEUPORABNO POLJE Mes_Let !!!!
            status_ttax = prihod.StanjeTTAX
            rna = prihod.RNA
            avans = prihod.AvansEUR
            cena = prihod.CENA
            st_odrasli = prihod.SO
            if st_odrasli == "" or st_odrasli == None:
                st_odrasli=0
            else:
                st_odrasli= int(st_odrasli)
            st_otroci = prihod.SOTR
            if st_otroci == "" or st_otroci ==None:
                st_otroci=0
            else:
                st_otroci= int(st_otroci)
            
            ttax = st_noci * (st_odrasli* 2 + st_otroci* 1)

            if rna == "AVANSOK":
                se_placati = str(round(float(cena) - float(avans)),2)
            elif rna == "NONREFOK" or rna == "ExpColl" or rna == "Virtual":
                if status_ttax == "Ttax NI VKLJ":
                    se_placati = ttax
                # ttax je že vključena
                else: 
                    se_placati = "0"
            # Refundable
            else:
                if status_ttax == "Ttax NI VKLJ":
                    se_placati = str(round(float(cena) + ttax, 2))
                # ttax je že vključena
                else: 
                    se_placati = str(round(float(cena),2))

            # Neuporabno polje Mes_Let !!!!!!!
            prihod.Mes_Let = se_placati 
            prihod.save()
                
        
        
        return self.prihodi_data
        #print(self.prihodi)

    def odhodi(self):
        self.odhodi_data = self.podatki.filter(do_dt= self.ob_datum)
        
        return self.odhodi_data
    
    def stayover(self):
        self.stayover_data= self.podatki.filter(Q(od_dt__lte=self.ob_datum) & Q(do_dt__gt=self.ob_datum))
        return self.stayover_data
        #for object in self.stayover:
        #    print(object.id, object.od, object.do_dt, object.imestranke)
    
    def menjave(self):
        self.menjave_data = self.stayover_data.annotate(datum_menjave=F("do_dt") - F("od_dt")).filter(datum_menjave__gt=timedelta(days=7)) 
        
        for object in self.menjave_data:
            object.datum_menjave = object.od_dt + timedelta(days= int(object.datum_menjave.days / 2)) 
            object.save()
        
        return self.menjave_data
        
        #for object in self.menjave_data:
        #    print(object.id, object.od, object.do_dt, object.imestranke, object.datum_menjave)
    
    def podatki_za_racune(self):
        list_dictov_racunov = []
        for odhod in self.odhodi_data:
            dict_podatki = {}
            if odhod.SO =="" or odhod.SO == None:
                odhod.SO = 0
            if odhod.SOTR =="" or odhod.SOTR == None:
                odhod.SOTR = 0
            st_noci = (odhod.do_dt - odhod.od_dt).days
            st_oseb_skupaj = int(odhod.SO) + int(odhod.SOTR)
            st_nocitev = st_noci * st_oseb_skupaj
            ttax = (int(odhod.SO) *2 + int(odhod.SOTR)*1) * st_noci
            if odhod.StanjeTTAX =="Ttax NI VKLJ":
                cena_na_nocitev= round((float(odhod.CENA))/st_nocitev/1.095, 4)
            else:
                cena_na_nocitev= round((float(odhod.CENA)-ttax)/st_nocitev/1.095, 4)
            dict_podatki["id"] = odhod.id
            dict_podatki["stsobe"] = odhod.stsobe
            dict_podatki["imestranke"] = odhod.imestranke
            dict_podatki["od"]= odhod.od
            dict_podatki["do"]= odhod.do
            dict_podatki["SO"]= odhod.SO
            dict_podatki["SOTR"] = odhod.SOTR
            dict_podatki["st_nocitev"] = st_nocitev
            dict_podatki["st_noci"] = st_noci
            dict_podatki["cena_na_nocitev"] = cena_na_nocitev 
            dict_podatki["agencija"] = odhod.agencija
            dict_podatki["RNA"] = odhod.RNA
            dict_podatki["CENA"] = odhod.CENA
            dict_podatki["TTAX"] =  ttax
            dict_podatki["StanjeTTAX"] = odhod.StanjeTTAX
            dict_podatki["DR"] = odhod.DR
            dict_podatki["zahteve"] = odhod.zahteve
            if odhod.RNA == "AVANSOK":
                dict_podatki["ze_placano"] = odhod.AvansEUR
            elif odhod.RNA == "NONREFOK":
                dict_podatki["ze_placano"] = odhod.CENA
            else:
                dict_podatki["ze_placano"] = ""

            list_dictov_racunov.append(dict_podatki) 

        return list_dictov_racunov
        
    
    def preracunaj_vrednost_nocitve(self, cena, stodr, stotr, stnoci, stnocitev, status_ttax):
        print(cena, stodr, stotr, stnoci, stnocitev, status_ttax)
        if stodr== "" or stodr== None:
                stodr= 0
        if stotr== "" or stotr== None:
            stotr= 0
        ttax = (int(stodr) *2 + int(stotr)*1) * stnoci
        
        st_oseb_skupaj = int(stodr) + int(stotr)
        stnocitev= st_oseb_skupaj * stnoci
        if status_ttax == "Ttax NI VKLJ":
            cena_na_nocitev= round((float(cena))/stnocitev/1.095, 4)
            
        else:
            cena_na_nocitev= round((float(cena)-ttax)/stnocitev/1.095, 4)
        print(cena_na_nocitev)
        return cena_na_nocitev, stnocitev, ttax
        


class Tabela_za_racun:        
    def __init__(self, gost, bar_narocila, ttax, rna):
        self.gost = gost
        self.bar_narocila = bar_narocila
        self.ttax= ttax
        self.rna= rna
    
    
    
    def tabela_nocitev_bar(self):
        tabela_nocitev_bar = []
        # vnesi podatke o gostu
        dict_gost = {"opis": "Nocitev (accommodation)",
                     "cena": self.gost.cena_nocitve,
                     "kolicina": self.gost.nocitev_skupaj,
                     "enota": "KOM",
                     "DDV" : 9.5,
                     "bruto_cena": round(float(self.gost.cena_nocitve) * 1.095, 2),
                     "bruto_znesek": round(float(self.gost.cena_nocitve) * 1.095 * self.gost.nocitev_skupaj ,2)

                     }
        tabela_nocitev_bar.append(dict_gost)
        # TUR TAX
        if self.gost.SO != "":
            dict_taxa_ODR = {"opis": "Turist. in promocijska taksa",
                     "cena": 2,
                     "kolicina": self.gost.SO * self.gost.st_noci,
                     "enota": "KOM",
                     "DDV" : 0,
                     "bruto_cena": 2,
                     "bruto_znesek": 2 * self.gost.SO * self.gost.st_noci

                     } 
            tabela_nocitev_bar.append(dict_taxa_ODR)
        
        
        if self.gost.SOTR != 0 and self.gost.SOTR != None :
            dict_taxa_OTR = {
                    "opis": "Turist. in promocijska taksa - otroci",
                    "cena": 1,
                    "kolicina": self.gost.SOTR * self.gost.st_noci,
                    "enota": "KOM",
                    "DDV" : 0,
                    "bruto_cena": 1,
                    "bruto_znesek": round(1 * self.gost.SOTR * self.gost.st_noci , 2 )

                     } 
            tabela_nocitev_bar.append(dict_taxa_OTR)
        #print(bar_narocila)
        
        if len(self.bar_narocila)!=0:
            for bar_narocilo in self.bar_narocila:
                dict_bar_narocilo = {
                    "opis": bar_narocilo["artikel__opis"], 
                    "cena": bar_narocilo["artikel__cena"], 
                    "kolicina": bar_narocilo["kolicina_skupaj"], 
                    "enota": bar_narocilo["artikel__enota"], 
                    "DDV": bar_narocilo["artikel__ddv"],  
                    "bruto_cena": float(bar_narocilo["artikel__cena"]) * (1+ int(bar_narocilo["artikel__ddv"])/100), 
                    "bruto_znesek": float(bar_narocilo["artikel__cena"]) * (1+ int(bar_narocilo["artikel__ddv"])/100) * bar_narocilo["kolicina_skupaj"], 
                }
                
                tabela_nocitev_bar.append(dict_bar_narocilo)
                dict_bar_narocilo={}
        
             
        
        #print(tabela_nocitev_bar)
        
        # Izračun ddv
        ddv_0= 0
        ddv_95= 0
        ddv_22= 0
        for x in tabela_nocitev_bar:
            if x["DDV"]==0:
                ddv_0 = ddv_0 + float(x["cena"]) * x["kolicina"]
            elif x["DDV"]== 9.5:
                ddv_95 = ddv_95 + float(x["cena"]) * x["kolicina"]
            elif x["DDV"]== 22:
                ddv_22 = ddv_22 + float(x["cena"]) * x["kolicina"]

        print(ddv_0, ddv_22, ddv_95)
        
        tabela_ddv = [["DDV 0%", ddv_0, ddv_0* 0, ddv_0+ddv_0*0],
                      ["DDV 9,5%", round(ddv_95,2), round(ddv_95* 0.095 ,2), round(ddv_95+ ddv_95 * 0.095 ,2)],
                      ["DDV 22%", round(ddv_22, 2), round(ddv_22* 0.22, 2), round(ddv_22+ ddv_22 * 0.22 ,2)]
                      ]
        

        # SKUPAJ
        skupaj_eur = ddv_0 + ddv_95 + ddv_22
        skupaj_ddv = ddv_0* 0 + ddv_95* 0.095 + ddv_22* 0.22
        
        odstej_eur= ""
        if self.rna == "AVANSOK":
            odstej_eur = self.gost.AvansEUR
        if self.rna == "NONREFOK" or self.rna == "ExpColl" or self.rna == "Virtual":
            if self.gost.StanjeTTAX == "Ttax NI VKLJ":
                odstej_eur = float(self.gost.CENA)
            else:
                odstej_eur = float(self.gost.CENA) - self.ttax

        za_placilo =  skupaj_eur+ skupaj_ddv- odstej_eur

       
            
        
        tabela_skupaj = [round(skupaj_eur, 2), round(skupaj_ddv, 2), round(odstej_eur, 2), round(za_placilo,2)]



        return tabela_nocitev_bar, tabela_ddv, tabela_skupaj
   




    ####
        """SEŠTEVANJE DVEH QS:
    queryset1 = MyModel.objects.filter(name__startswith='A')
    queryset2 = MyModel.objects.filter(name__startswith='B')

    result_queryset = queryset1.union(queryset2 """






    ### PRIMERI CLASS ####
    """class Item:
    pay_rate = 0.8 # the pay rate after 20% discount
    def __init__(self, name , price , quantity ):
        # VALIDATION of received arguments
        assert price>=0, f'Cena ni večja od 0 !!!, saj je vrednost {price}'
        
        # Assign to SELF OBJECT
        self.name=name
        self.price=price
        self.quantity=quantity
        
    def calculate_total_price(self):
        return self.price*self.quantity
    
    def apply_discount(self):
        return Item.pay_rate * self.price * self.quantity

        
        

    item1=Item("Iphone",22,5)
    print(item1.calculate_total_price())  # kličes metodo calculete... from instance. Pyton
                                    # passes the object as the first argumet every time
                                    # ne moremo delati metod, ki nikoli ne bodo dobile parametrov


    # Uporaba CLASS ATTRIBUTA (pay_rate)
    print(item1.apply_discount())

    ######################################################
    class Car1():
        wheels=4
        
        def __init__(self,color,typeCar,seats):
            self.color=color
            self.typeCar=typeCar
            self.seats=seats
            print("init was exec")

    

    c1=Car1("red","vw","leather")
    #c2=Car("blue","audi")
    #
    # c3=Car("green","merc")

    print(c1.color,c1.typeCar,c1.seats)



    class Car():        #Car je NAME of class
        wheels=4        #wheels je PROPERTY of class
                        # c1 je OBJECT , ki nastane po matrici class-a
                        #__init__ določi vrednosti Object's Properties
                        # SELF parameter je referenca na TRENUTNI class in ima dostop do vseh VARIABLES v classu
        def __init__(self,color,typeCar,seats):
            self.color=color
            self.typeCar=typeCar
            self.seats=seats
            print("init was exec")

    

    c1=Car("red","vw","leather")
    #c2=Car("blue","audi")
    #c3=Car("green","merc")

    print(c1.color,c1.typeCar,c1.seats)

    #______________________

    print()
    print("NASLEDNJI PRIMER")
    print()

    class imena():
        def __init__(self,ime, priimek):
            self.ime=ime
            self.priimek=priimek


    oseba1=imena("peter","gašperin")
    print(oseba1.ime+" "+oseba1.priimek)


    print()
    print("OBJECT METHODS - imaš funkcijo, ki se navezuje na prejšnjo")
    print("SELF je parameter, ki se navezuje na trenutni class in ima dostop do vseh variabel v classu")
    print()


    class test1():
        def __init__(self,ime,priimek):
            self.ime=ime
            self.priimek=priimek

        def Tiska_text(self):
            print("Moje ime je "+ self.ime)

    oseba2=test1("Peter","Gašperin")
    oseba2.Tiska_text()


    #CLASS INHERITANCE - posvojen class Parent/Child
    print()
    print("CLASS INHERITANCE - posvojen class Parent/Child")
    print("ko dodaš __init__ childu, le ta povozi __init__ od parenta")

    class Osebek():
        def __init__ (self,ime,priimek):
            self.ime=ime
            self.priimek=priimek

        def tiskanje(self):
            print("moje ime je ",self.ime)

    class Child(Osebek):
        def __init__ (self,ime,priimek,starost):
            super().__init__(ime, priimek)
            self.tvojastarost=starost
        
        def tiskanjeChild(self):
            print(self.ime,self.priimek,self.tvojastarost)


    oseba1=Osebek("Peter","Gašperin")
    oseba1.tiskanje()
    print(oseba1.priimek)
    osebaChild=Child("Pavel","Novak","22")
    osebaChild.tiskanjeChild()
    """