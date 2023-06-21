# pylint: disable=E0401,W0401
#from django.db.models import Value
#from django.db import models
#from django.db.models import Q, Count, Sum, F
from datetime import datetime, timezone, timedelta

from Aplikacija.models import *
from Rezervacije.models import VnosGostov

import numpy
from . import graf
import pandas as pd


class App_podatki:
    def __init__(self, ob_datum, vir):
        self.ob_datum = ob_datum
        self.vir = vir
        
        
        vhodni_podatki= VnosGostov.objects.filter(status_rez= "rezervirano")
        # Pretvori Queryset >> Pandas
        data = list(vhodni_podatki.values())
        self.izbrani_podatki = pd.DataFrame.from_records(data=data)
        
        
        
        sobe=[10,11,12,20,21,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,50,51,52]

        # Pretvori ceno iz object v numeric - float64
        self.izbrani_podatki["CENA"] = pd.to_numeric(self.izbrani_podatki["CENA"])         #!!!!!!!!!!!!!!!!!
        #print(izbraniP.dtypes)

        # Zaradi varnosti, pretori datume v Pandas datume
        #izbraniP["datumvnosa"]=pd.to_datetime(izbraniP["datumvnosa"]).dt.normalize()
        self.izbrani_podatki["od"]=pd.to_datetime(self.izbrani_podatki["od"],format="%d.%m.%Y").dt.normalize()
        self.izbrani_podatki["do"]=pd.to_datetime(self.izbrani_podatki["do"],format="%d.%m.%Y").dt.normalize()

        # Dodaten stolpec "stnocitev"
        self.izbrani_podatki["stnocitev"]=(self.izbrani_podatki["do"]-self.izbrani_podatki["od"]).dt.days # odstrani besedo days

        self.obdatum=self.ob_datum
        #self.obdatum=pd.to_datetime(self.obdatum,format=("%d.%m.%Y"))
       
        # JUTRI
        obdanPlus1dan=self.obdatum+ timedelta(days=1)
        self.PRIHODI=self.izbrani_podatki[self.izbrani_podatki["od"]==self.obdatum]
        
        # ODHODI
        self.ODHODI=self.izbrani_podatki[self.izbrani_podatki["do"]==self.obdatum]

        #ODHODI JUTRI - potrebujem za priprabo posteljnine po etažah
        self.odhodi_jutri=self.izbrani_podatki[self.izbrani_podatki["do"]==obdanPlus1dan]
        self.odhodi_jutri=self.odhodi_jutri.loc[:,["stsobe","SO"]]
        self.odhodi_jutri=self.odhodi_jutri.sort_values(by="stsobe",ascending=True)
        #print(ODHODI_JUTRI)

        #Izpiši STAYOVER

        self.STAYOVER=self.izbrani_podatki[(self.izbrani_podatki["od"]<self.obdatum) & (self.izbrani_podatki["do"]>self.obdatum)]
        #Ustvari stolpec st nocitev


        # MENJAVA POSTELJNINE
        #Izloči samo sobe, ki imajo več kot 7 nočitev
        stayover_mp=self.STAYOVER[self.STAYOVER["stnocitev"]>7]  #_MP = menjava posteljnine
        
        L_SobeMenjava=[]
        # Iter po vsaki vrstici dataframe posebej 
        for soba in range(stayover_mp.shape[0]):
            MenjVrstica=stayover_mp.iloc[soba,:]
        
            StSobeMenj=MenjVrstica["stsobe"]
            OdDatMenj=MenjVrstica["od"]
            #DoDatMenj=MenjVrstica["do"]
            STNocMenj=MenjVrstica["stnocitev"]
            ZaokrozenoDeljenje=int((numpy.round((STNocMenj/2),0))) # !!!!!!!!!!!
            # Dodaj zaokroženo deljenje OD dat in dobiš datum, ko naj bo menjava
            DatumZaMenjavo=OdDatMenj+timedelta(days=ZaokrozenoDeljenje)
            # če je datum za menjavo enak OBDAT, daj sobo v list
            if ((DatumZaMenjavo-self.obdatum).days)==0:
                L_SobeMenjava.append(StSobeMenj)
        
        
        # iz tabele Stayover izloči samo sobe, ki imajo menjavo
        
        self.MENJAVEPOSTELJN=stayover_mp[stayover_mp["stsobe"].isin(L_SobeMenjava)] # !!!!!!!!!
        self.MENJAVEPOSTELJN=self.MENJAVEPOSTELJN[["stsobe"]]
        
        
        ###################################################################

        #Kdaj NASLEDNJI PRIHOD?
        #Katere sobe so: Prihod, stay over - te lahko izločiš
        #Potencialne sobe, ki imajo naslednji prihod (vse sobe - prihod+stayover)
        #združi prihod in stayover
        self.ZDRprh_styov=pd.concat([self.PRIHODI,self.STAYOVER],axis=0) #axis=0 je leplejnje po vertikali- stolpci
        
        #Pridobi list s številkami sob v združeni tabeli - to so sobe, ki jih ni treba spremljati
        SOBEprh_styov=self.ZDRprh_styov.loc[:,["stsobe"]]

        #Pretvori stolpec št sobe v LIST
        ListSobeprh_styov=SOBEprh_styov["stsobe"].tolist()

        #Iz lista SOBE naredi nov list, ki naj ohrani samo sobe, ki jih je smiselno spremljati
        SobeZaNaslPrih=[]
        for x in sobe:  # sobe je list vseh sob, ki je definiran na vrhu tega programa
            if x not in ListSobeprh_styov:
                SobeZaNaslPrih.append(x)

        #Iz glavnega seznama izbraniP izloči samo datume, ki so od obdatum dalje
        #in ki vsebujejo samo sobe iz LISTA: SobeZaNaslPrih

        PrihodnjiPrihodi=self.izbrani_podatki[self.izbrani_podatki["od"]>self.obdatum]
        PRPR=PrihodnjiPrihodi[PrihodnjiPrihodi["stsobe"].isin(SobeZaNaslPrih)]
        PRPR=PRPR.sort_values(by="od",ascending=True)

        #Dobil seznam sob, ki imajo v prihodnje prihod. dobiti treba sobe, ki imajo najprej prihod 

        #Dobi unique vrednosti v zadnji tabeli in daj v LIST. Na osnovi tega lista filtriraj vse sobe (od Obdan dalje), in skopiraj vrstico z najnižjim datumom-
        # To je naslednji prihod

        unikatne_st_sob=pd.unique(PRPR["stsobe"]).tolist()  #!!!!!!

        #Izdelaj prazno tabelo, ki naj ima iste stolpce kot izbraniP
        self.Tabela_prihodnjiPrih =pd.DataFrame(columns=self.izbrani_podatki.columns)

        for soba in unikatne_st_sob:
            ArrayprvaVrstica=(PRPR[PRPR["stsobe"]==soba])
            PrvaVrstic=ArrayprvaVrstica.iloc[[0]] #Izloči samo prvo vrstico
            #Dodaj prvo vrstico v prazno tabelo
            self.Tabela_prihodnjiPrih=self.Tabela_prihodnjiPrih.append(PrvaVrstic,ignore_index=True)
            
        if self.Tabela_prihodnjiPrih.empty:
            pass
        else:
            self.Tabela_prihodnjiPrih["DniDoNaslPrih"]=(self.Tabela_prihodnjiPrih["od"]-self.obdatum).dt.days
            self.Tabela_prihodnjiPrih=self.Tabela_prihodnjiPrih.loc[:,["stsobe","DniDoNaslPrih","od"]]
            #print(Tabela_prihodnjiPrih)
        
        ###################################KONEC PRIHODNJI PRIHOD




        ###################### KATERE SOBE SO BILE VČERAJ PRAZNE? 

        #naredi Tabela: odhodi + stayover
        # izdelaj LIST seznam sob, ki so v skupni tabeli ODH-SYOV
        # v glavni tabeli s pomočjo LIST seznam sob pridobi Tabelo z rez., ki
        # imajo odhod 1 dan pred Obdan 
        #    


        self.ZDRodh_styov=pd.concat([self.ODHODI,self.STAYOVER],axis=0)

        ListOdhStyov=self.ZDRodh_styov["stsobe"].tolist()
        #print(ListOdhStyov)
        #Izdelaj tabelo s številkami sob, ki so bile danes proste

        List_sobe_vcer_przn=[]
        for soba in sobe:
            if soba not in ListOdhStyov:
                List_sobe_vcer_przn.append(soba)


        # Iz pridobljenega lista izdelaj pd-tabelo, ki ima samo stolpec s številkami
        # včeraj praznih sob

        self.Tabela_vceraj_praznih_sob=(pd.DataFrame(List_sobe_vcer_przn, columns=["stsobe"]))


        ########################## KONEC KATERE SOBE SO BILE VČERAJ PRAZNE


        # IZDELAVA TABELE Z ODHODI Z USTREZNIMI CENAMI GLEDE NA TO ALI IMA REZERVACIJA VKLJUČENO TTAXO ALI NE
        
        odhodi_r=self.ODHODI.copy()
        odhodi_r = odhodi_r.sort_values("stsobe")
        #Pretvori date v string  Datetime to string !!!!!!!!!!!!!
        odhodi_r["od"] = odhodi_r["od"].apply(lambda x: datetime.strftime(x, '%d.%m.%y'))
        odhodi_r["do"] = odhodi_r["do"].apply(lambda x: datetime.strftime(x, '%d.%m.%y'))

        
        pandas_vrstica=0
        if self.ODHODI.empty:
            #Izdelati moraš prazno tabelo, drugače poizvedba od soseda zablokira program
            # To tabelo moraš izdelati zato, ker cena na nočitev je različna, če je TTax vključena ali ne
            # verjetno bi se dalo to narediti s pandas, ampak ta način je, da računa ceno na nočitev za posamzno rezervacijo posebej
            stolpci=["id","stsobe","imestranke","agencija","od","do","stnocitev","CENAnanoc","StanjeTTAX","DR","RNA","CENA"]
            List_indx_sob=[]
            i=0
            while i<self.ODHODI.shape[0]:
                List_indx_sob.append(i)
                i+=1
            self.T_ODHODI_Racuni=pd.DataFrame(columns=[stolpci],index=[List_indx_sob])
            
            #pass
            # print('NI RAČUNOV')
        else:
            self.ODHODI=self.ODHODI.sort_values(by="stsobe",ascending=True)
            
            
            # Izdelaj prazno Pandas tabelo z imeni stolpcev=Fildi, indexi so številke 1,2,3...
            # To tabelo moraš itdelati zato, ker cena na nočitev je različna, če je TTax vključena ali ne
            # verjetno bi se dalo to narediti s pandas, ampak ta način je, da računa ceno na nočitev za posamzno rezervacijo posebej
            
            stolpci=["id","stsobe","imestranke","agencija","od","do","stnocitev","CENAnanoc","StanjeTTAX","DR","RNA","CENA"]
            List_indx_sob=[]
            i=0
            
            while i<self.ODHODI.shape[0]:
                List_indx_sob.append(i)
                i+=1
            self.T_ODHODI_Racuni=pd.DataFrame(columns=[stolpci],index=[List_indx_sob])
            #print(T_ODHODI_Racuni)

            for i in range(odhodi_r.shape[0]): #loop skozi vrstice v tabeli VSEH odhodov
                odhodi_r1=odhodi_r.iloc[i,:]
                SifraVnosa=odhodi_r1["id"]
                StSobe=odhodi_r1["stsobe"]
                ImeStranke=odhodi_r1["imestranke"]
                Agencija=odhodi_r1["agencija"]
                StOseb=odhodi_r1["SO"]
                OdDat=odhodi_r1["od"]
                DoDat=odhodi_r1["do"]
                CenaSK=(odhodi_r1["CENA"])
                NocitecTOT=odhodi_r1["stnocitev"]*StOseb
                Rna=odhodi_r1["RNA"]
                Drzava=odhodi_r1["DR"]
                StanjeTtax=odhodi_r1["StanjeTTAX"]
                if StanjeTtax =="Ttax NI VKLJ":
                    StanjeTtax="NI vključena ttaxa!"
                    CenaNaNoc=(CenaSK)/NocitecTOT
                else:
                    StanjeTtax="Ttax JE v ceni"
                    CenaNaNoc=(CenaSK-(2*StOseb))/NocitecTOT
                Fildi=[SifraVnosa,StSobe,ImeStranke,Agencija,
                OdDat,DoDat,NocitecTOT,CenaNaNoc,StanjeTtax,Drzava,Rna,CenaSK]
                
                
                
                
                for j in range(len(Fildi)):
                    #ws.cell(row=VRSTICA,column=j+1).value=Fildi[j]
                    
                    # V prazno pandas tabelo dodajaj elemente:
                    self.T_ODHODI_Racuni.iat[pandas_vrstica,j]=Fildi[j]
                
                pandas_vrstica+=1    
                
        # Definiraj T_GRAF # dodati moraš dneve, da se na tabeli graf v excelu ObDatum pojavi na skrajno levi strani
        self.T_GRAF= graf.IzdelavaGrafa(df_data= self.izbrani_podatki, 
                                        DatumObravnave= self.obdatum+timedelta(days=14), 
                                        Vir= "DN")  #"R_Optimi") r_optimi je za "glavni" graf, DN pa za graf v app.
        
       

    ##############################################################
    ######  PODATKI ZA WEB APLIKACIJO ###########################
    ##############################################################
    
    def PodatkiZaWebApplic(self):
        
        ###### Pošlji Obravnavani datum:
        #############################
        #self.ob_datum
        
        ##### Tabela sob Stayower, odhod, menjava; #############
        ########################################################

        T_SobeODH_STOW_MENJ = self.STAYOVER[["stsobe"]]
        T_SobeODH_STOW_MENJ["Akcija"]="pospravi"
        T_SobeODH_STOW_MENJ["Za_Oseb"] = 0
        T_SobeODH_STOW_MENJ["Status"] = ""
        T_SobeODH_STOW_MENJ["DatumVnosa"] = self.STAYOVER[["datumvnosa"]]
        T_SobeODH_STOW_MENJ["Ime"] = self.STAYOVER[["imestranke"]]
        T_SobeODH_STOW_MENJ["Agencija"] = self.STAYOVER[["agencija"]]
        T_SobeODH_STOW_MENJ["Od"] = self.STAYOVER[["od"]]
        T_SobeODH_STOW_MENJ["Do"] = self.STAYOVER[["do"]]
        T_SobeODH_STOW_MENJ["Cena"] = self.STAYOVER[["CENA"]]
        T_SobeODH_STOW_MENJ["Oseb"] = self.STAYOVER[["SO"]]
        T_SobeODH_STOW_MENJ["Tip"] = self.STAYOVER[["tip"]]
        T_SobeODH_STOW_MENJ["Drzava"] = self.STAYOVER[["DR"]]
        T_SobeODH_STOW_MENJ["Zahteve"] = self.STAYOVER[["zahteve"]]
        T_SobeODH_STOW_MENJ["Alergije"] = self.STAYOVER[["Alergije"]]
        T_SobeODH_STOW_MENJ["RNA"] = self.STAYOVER[["RNA"]]
        T_SobeODH_STOW_MENJ["uni_koda"] = self.STAYOVER[["id"]]       #[["sifravnosa"]]


        
        # List sob, kjer je menjava (po 7 dneh)
        L_sobeMenjava = self.MENJAVEPOSTELJN["stsobe"].tolist()

        # Če je v tabeli T_SobeODH_STOW_MENJ , jo v stolpcu Akcija, označi "menjava"       
        L_vseSobe = T_SobeODH_STOW_MENJ["stsobe"].tolist()
        
        for x in range(0, len(L_sobeMenjava)):
            if L_sobeMenjava[x] in L_vseSobe:
                Indeks = L_vseSobe.index(L_sobeMenjava[x])
                T_SobeODH_STOW_MENJ.iat[Indeks, 1]= "menjava"

        
        # Dodaj odhode in v stolpec "Za oseb" dodaj za koliko oseb mora biti pripravljena soba
        #print(self.ODHODI[["stsobe"]])
        T_Odhodi = self.ODHODI[["stsobe"]]
        T_Odhodi["Akcija"] = "odhod"
        T_Odhodi["Za_Oseb"] = 0
        T_Odhodi["Status"] = ""
        T_Odhodi["DatumVnosa"] = self.ODHODI[["datumvnosa"]]
        T_Odhodi["Ime"] = self.ODHODI[["imestranke"]]
        T_Odhodi["Agencija"] = self.ODHODI[["agencija"]]
        T_Odhodi["Od"] = self.ODHODI[["od"]]
        T_Odhodi["Do"] = self.ODHODI[["do"]]
        T_Odhodi["Cena"] = self.ODHODI[["CENA"]]
        T_Odhodi["Oseb"] = self.ODHODI[["SO"]]
        T_Odhodi["Tip"] = self.ODHODI[["tip"]]
        T_Odhodi["Drzava"] = self.ODHODI[["DR"]]
        T_Odhodi["Zahteve"] = self.ODHODI[["zahteve"]]
        T_Odhodi["Alergije"] = self.ODHODI[["Alergije"]]
        T_Odhodi["RNA"] = self.ODHODI[["RNA"]]
        T_Odhodi["uni_koda"] = self.ODHODI[["id"]]   #[["sifravnosa"]]
        
        T_SobeODH_STOW_MENJ=pd.concat([T_SobeODH_STOW_MENJ,T_Odhodi],axis=0).sort_values("stsobe")
        T_SobeODH_STOW_MENJ.rename(columns={'stsobe': 'Soba',}, inplace=True, errors='raise')
        
        # Dodaj stolpce, ki jih bo izpolnila aplikacija
        T_SobeODH_STOW_MENJ["StatusZajtrk"] = ""
        T_SobeODH_STOW_MENJ["status_zajtrk_num"] = 0
        T_SobeODH_STOW_MENJ["status_num"] = 0
        T_SobeODH_STOW_MENJ["cas_zajtrka"] = None
        T_SobeODH_STOW_MENJ["cas_ciscenja"] = None
        
        
        # Pretvori datume v strf
        T_SobeODH_STOW_MENJ["Do"] = T_SobeODH_STOW_MENJ["Do"].dt.strftime("%d.%m.")
        T_SobeODH_STOW_MENJ["Od"] = T_SobeODH_STOW_MENJ["Od"].dt.strftime("%d.%m.")
        
        #Ponovno izdelaj L_vseSobe
        L_vseSobe = T_SobeODH_STOW_MENJ["Soba"].tolist()

        
        
        ###### TABELA Prihodi #########################
        ###############################################

        T_Prihodi = self.PRIHODI[["id", "stsobe","SO", "datumvnosa", "imestranke", "agencija","od","do","CENA","tip","DR","zahteve","Alergije","RNA", "StanjeTTAX"]]
        L_sobePrihodi = T_Prihodi["stsobe"].tolist()
        L_stOsebPrihodi = T_Prihodi["SO"].tolist()
        # POSPRAVLJANJE T_SobeODH_STOW_MENJ  Za koliko oseb naj čistilke pripravijo, če je danes prihod:
        for i in range(0, len(L_sobePrihodi)):
            if L_sobePrihodi[i] in L_vseSobe:
                indeks = L_vseSobe.index(L_sobePrihodi[i])
                T_SobeODH_STOW_MENJ.iat[indeks, 2] = L_stOsebPrihodi[i]
        
        
        
        self.T_Prihodi1 = T_Prihodi.copy()
        
        # Dodaj stolpce, ki jih bo izpolnila aplikacija
        self.T_Prihodi1["Status"] = ""
        self.T_Prihodi1["cas_checkin"] = None #datetime.now()
        
        
        # PRIHODI Če je danes v sobo prihod, ta soba pa je bila včeraj prazna, to označi v PRIHODI/Status : "Bila prazna"
        
        for i in range(len(L_sobePrihodi)):
            if L_sobePrihodi[i] not in L_vseSobe:
                self.T_Prihodi1.iat[i, self.T_Prihodi1.columns.tolist().index("Status")] = "Bila prazna"

        #print(self.T_Prihodi1)
        self.T_Prihodi1.rename(columns={"id": "uni_koda",
                                    "datumvnosa": "DatumVnosa",
                                    "stsobe": "Soba", 
                                    "SO": "St_Oseb",
                                    "imestranke":"Ime",
                                    "od":"Od",
                                    "do":"Do",
                                    "CENA":"Cena",
                                    "tip":"Tip",
                                    "DR":"Drzava",
                                    "zahteve":"Zahteve",
                                    "StanjeTTAX":"Ttax",
                                    "agencija": "Agencija",
                                    }, inplace=True, errors="raise")
        # Dodaj stolpce:
        self.T_Prihodi1["st_noci"] = (self.T_Prihodi1["Do"] - self.T_Prihodi1["Od"]).dt.days
        
        self.T_Prihodi1["Do"] = self.T_Prihodi1["Do"].dt.strftime("%d.%m.")
        self.T_Prihodi1["Od"] = self.T_Prihodi1["Od"].dt.strftime("%d.%m.")
        self.T_Prihodi1=self.T_Prihodi1.sort_values("Soba")
        # Odstrani stolpec uni_koda
        #self.T_Prihodi1=self.T_Prihodi1.drop("uni_koda", axis=1)
        #print(T_Prihodi)

        #print(T_SobeODH_STOW_MENJ)
        #self.T_SobeODH_STOW_MENJ = T_SobeODH_STOW_MENJ.copy()
        

        ### GRAF ############
        #####################
        
        
        ListVrstice = [i for i in range(31)]
        ListStolpi = ["S" + str(i) for i in range(20)]
        self.T_Graf = pd.DataFrame(index=ListVrstice ,columns=ListStolpi)
        # print(self.T_Graf.iloc[0:27,1:20])
        # print(self.T_GRAF)#.iloc[0:27,2:21])
        self.T_Graf.iloc[0:27,0] = self.T_GRAF.iloc[0:27,0]
        self.T_Graf.iloc[0:27,1:20] = self.T_GRAF.iloc[0:27,1:20]             #[0:27,20:39]
        self.T_Graf.iloc[27:31,1:20] = self.T_GRAF.iloc[27:31,1:20]                       #[29:33,20:39]
        self.T_Graf=self.T_Graf.fillna("")
        self.T_Graf.iat[27,0] = "Zaj"
        self.T_Graf.iat[28,0] = "Men"
        self.T_Graf.iat[29,0] = "StS"
        self.T_Graf.iat[30,0] = "Prh"
        
        
        ### PRAZNE SOBE ############
        ############################
        # PODATKI
        
        T_Arhiv = self.izbrani_podatki
        
        # POPRAVI TIP DATUMOV
        T_Arhiv["od"]=pd.to_datetime(T_Arhiv["od"], format="%d.%m.%Y")
        T_Arhiv["do"]=pd.to_datetime(T_Arhiv["do"], format="%d.%m.%Y")
        T_Arhiv["datumvnosa"]=pd.to_datetime(T_Arhiv["datumvnosa"], format="%d.%m.%Y")
        T_Arhiv= T_Arhiv.sort_values("od")
        # ŠTEVILKE SOB
        L_StSob = [10,11,12,20,21,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,50,51,52]

        # OB DATUM
        
        # STAYOVER+PRIHODI
        T_StayoverPrih = pd.DataFrame()
        L_StayoverPrihod =[]
        L_tupl_PrznSob = []
        for stSobe in L_StSob:
            T_PosameznaSobaVSE = T_Arhiv[T_Arhiv["stsobe"]== stSobe]
            T_StayoverPrih = T_PosameznaSobaVSE.copy()
            T_StayoverPrih = T_StayoverPrih[(T_StayoverPrih["od"]<= self.obdatum) & (T_StayoverPrih["do"]> self.obdatum)]
            #print(T_StayoverPrih[["stsobe","od","do"]])
            #print(type(T_StayoverPrih))
            # PRAZNE SOBE NA OBDAN
            if T_StayoverPrih.empty:
                
                # DO KDAJ JE SOBA PRAZNA
                T_NaslPrihTeSobe = T_PosameznaSobaVSE[T_PosameznaSobaVSE["od"]> self.obdatum] 
                naslednjiDatPrih = T_NaslPrihTeSobe.iloc[0, T_NaslPrihTeSobe.columns.get_loc("od")]
                stDniDoNaslPrih = (naslednjiDatPrih - self.obdatum).days
                L_tupl_PrznSob.append((stSobe, naslednjiDatPrih.strftime(format="%d.%m."), stDniDoNaslPrih))
            else:
                L_StayoverPrihod.append(stSobe)
        
        self.T_PrazneSobe = pd.DataFrame(L_tupl_PrznSob, columns=["Soba", "NaslPrh", "DniDoPrih"])
        #print(T_PrazneSobe)

        # V TABELAH self.T_Prihodi1 IN self.T_SobeODH_STOW_MENJ preveri STARO STANJE v aplikaciji, in ga dodaj novim tabelam
        # to je, ko tekom dneva pride do sprememb v rezervaciji, zato je treba že zbrane podatke iz aplikacije 
        # upariti z novimi podatki, ki prihajajo v aplikacijo
        
        obravnavani_datum_star = ObravnavaniDatum.objects.all().first()
        obravnavani_datum_star = obravnavani_datum_star.DatumObravnavani
        #print(obravnavani_datum_star)
        
        pospravljanje_star= Pospravljanje.objects.all()
        # Pretvori Queryset >> Pandas
        data = list(pospravljanje_star.values())
        T_SobeODH_STOW_MENJ_star = pd.DataFrame.from_records(data=data)
        #print(T_SobeODH_STOW_MENJ_star)
        
        
        
        prihodi_star = PospravljanjePrihodi.objects.all().values()
        # Pretvori Queryset >> Pandas
        data = list(prihodi_star.values())
        T_Prihodi1_star = pd.DataFrame.from_records(data=data)
        #print(T_Prihodi1_star)







        #if datetime.strptime(self.obdatum, "%d.%m.%Y").date() == datetime.strptime(obravnavani_datum_star, "%d.%m.%Y").date():
        
        if self.obdatum.date() == datetime.strptime(obravnavani_datum_star, "%d.%m.%Y").date():
        
            # V novi tabeli greš skozi vse sobe in primerjaš podatke s staro tabelo
            
            #############################################################################
            # POSPRAVLJANJE - SINHRONIZACIJA NOVEGA STANJA Z ŽE VNEŠENIMI PODATKI V APP
            #print("T_odhStayov_nova")
            #print(T_SobeODH_STOW_MENJ)
            
            for index, value in T_SobeODH_STOW_MENJ["uni_koda"].iteritems():
             
                
                
                if value in T_SobeODH_STOW_MENJ_star["uni_koda"].astype(int).values:
                    #Iskanje indexa te rezervacije v stari tabeli
                    index_star = T_SobeODH_STOW_MENJ_star["uni_koda"].astype(int).index[T_SobeODH_STOW_MENJ_star["uni_koda"].astype(int)== value][0]
                    
                
                    T_SobeODH_STOW_MENJ.loc[index, "StatusZajtrk"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "StatusZajtrk"]
                    T_SobeODH_STOW_MENJ.loc[index, "Akcija"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "Akcija"]
                    T_SobeODH_STOW_MENJ.loc[index, "Status"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "Status"]
                    T_SobeODH_STOW_MENJ.loc[index, "status_zajtrk_num"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "status_zajtrk_num"]
                    #T_SobeODH_STOW_MENJ.loc[index, "cas_zajtrka"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "cas_zajtrka"]
                    T_SobeODH_STOW_MENJ.loc[index, "status_num"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "status_num"]



                    if T_SobeODH_STOW_MENJ_star.loc[index_star, "cas_ciscenja"] == None:
                        T_SobeODH_STOW_MENJ.loc[index, "cas_ciscenja"] = None
                    else:
                        T_SobeODH_STOW_MENJ.loc[index, "cas_ciscenja"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "cas_ciscenja"]
                    
                    if T_SobeODH_STOW_MENJ_star.loc[index_star, "cas_zajtrka"] == None:
                        T_SobeODH_STOW_MENJ.loc[index, "cas_zajtrka"] = None
                    else:
                        T_SobeODH_STOW_MENJ.loc[index, "cas_zajtrka"] = T_SobeODH_STOW_MENJ_star.loc[index_star, "cas_zajtrka"]
                    
                    
                    
                    T_SobeODH_STOW_MENJ["StatusZajtrk"]= T_SobeODH_STOW_MENJ["StatusZajtrk"].fillna("")
                    T_SobeODH_STOW_MENJ["Akcija"]= T_SobeODH_STOW_MENJ["Akcija"].fillna("")
                    T_SobeODH_STOW_MENJ["Status"]= T_SobeODH_STOW_MENJ["Status"].fillna("")
                    #T_SobeODH_STOW_MENJ["cas_ciscenja"]= T_SobeODH_STOW_MENJ["cas_ciscenja"].fillna("")
                    T_SobeODH_STOW_MENJ["status_zajtrk_num"]= T_SobeODH_STOW_MENJ["status_zajtrk_num"].fillna("")
                    #T_SobeODH_STOW_MENJ["cas_zajtrka"]= T_SobeODH_STOW_MENJ["cas_zajtrka"].fillna("")
                    T_SobeODH_STOW_MENJ["status_num"]= T_SobeODH_STOW_MENJ["status_num"].fillna("")
                    ###T_odhStayov["cas_ciscenja"].replace("NaT",0)

            print("T_odhStayov_stara")
            print(T_SobeODH_STOW_MENJ_star[["cas_zajtrka", "cas_ciscenja"]])
            print("T_odhStayov_nova")
            print(T_SobeODH_STOW_MENJ[["cas_zajtrka", "cas_ciscenja"]])
            
            #Odstrani NAN iz predelane T_prihodi

            ######################################################
            # PRIHODI - SINHRONIZACIJA NOVEGA STANJA Z ŽE VNEŠENIMI PODATKI V APP
            for index, value in self.T_Prihodi1["uni_koda"].iteritems():
                
                if value in T_Prihodi1_star["uni_koda"].values:
                    #Iskanje indexa te rezervacije v stari tabeli
                    index_star = T_Prihodi1_star["uni_koda"].index[T_Prihodi1_star["uni_koda"]== value][0]
                    
                
                    self.T_Prihodi1.loc[index, "Status"] = T_Prihodi1_star.loc[index_star, "Status"]
                    self.T_Prihodi1.loc[index, "StatusCheckIn"] = T_Prihodi1_star.loc[index_star, "StatusCheckIn"]
                    self.T_Prihodi1.loc[index, "cas_checkin"] = T_Prihodi1_star.loc[index_star, "cas_checkin"]
                    
                    # Odstrani nan
                    self.T_Prihodi1["Status"]= self.T_Prihodi1["Status"].fillna("")
                    self.T_Prihodi1["StatusCheckIn"]= self.T_Prihodi1["StatusCheckIn"].fillna("")
                    self.T_Prihodi1["cas_checkin"]= self.T_Prihodi1["StatusCheckIn"].fillna("")
                    

            # print("prihodi_stara")
            # print(T_Prihodi1_star)
            # print("prihodi_nova")
            # print(self.T_Prihodi1)
            
            #Odstrani NAN iz predelane T_prihodi
            
            ### Konec PRIHODI
        else:
            print("Datuma nista enaka")


        

































        ############################
        # VRNI POROČILA V BAZO:  ##
        ############################


        # Pretvori Padas >> Queryset
        # Ob Datum
        obdatum = ObravnavaniDatum.objects.get(Naziv= "Ime")
        obdatum.DatumObravnavani = datetime.strftime(self.ob_datum, "%d.%m.%Y")
        obdatum.save() 
        

        Pospravljanje.objects.all().delete()
        my_dict = T_SobeODH_STOW_MENJ.to_dict(orient= "records")
        my_instances = [Pospravljanje(**d) for d in my_dict]
        Pospravljanje.objects.bulk_create(my_instances)


        PospravljanjePrihodi.objects.all().delete()
        my_dict = self.T_Prihodi1.to_dict(orient= "records")
        my_instances = [PospravljanjePrihodi(**d) for d in my_dict]
        PospravljanjePrihodi.objects.bulk_create(my_instances)
        

        Graf.objects.all().delete()
        my_dict = self.T_Graf.to_dict(orient= "records")
        my_instances = [Graf(**d) for d in my_dict]
        Graf.objects.bulk_create(my_instances)

        PrazneSobe.objects.all().delete()
        my_dict = self.T_PrazneSobe.to_dict(orient= "records")
        my_instances = [PrazneSobe(**d) for d in my_dict]
        PrazneSobe.objects.bulk_create(my_instances)

        return
    
        
        
        
        
        

   
   #########################################################################
   ##########  KONEC WEB APLIKACIJE #######################################
   ########################################################################



    """def VrniPorocila(self):
        # VRNI POROČILA SOSEDU Rez_DN_Pregled
        if self.vir=="PrihodiDN":  # za Rez_DN_Pregled
            self.PRIHODI= self.PRIHODI.sort_values(by="stsobe")
            return self.PRIHODI
        elif self.vir=="StayoverDN": # za Rez_DN_Pregled
            self.STAYOVER["od"] = self.STAYOVER["od"].apply(lambda x: dt.datetime.strftime(x, '%d.%m.%y'))
            self.STAYOVER["do"] = self.STAYOVER["do"].apply(lambda x: dt.datetime.strftime(x, '%d.%m.%y'))
            self.STAYOVER= self.STAYOVER.sort_values(by="stsobe")
            return self.STAYOVER        
        elif self.vir=="RacuniDN": # za Rez_DN_Pregled
            #self.T_ODHODI_Racuni.sort_values(by="stsobe")
            #print(type(self.T_ODHODI_Racuni))
            #print((self.T_ODHODI_Racuni))
            return self.T_ODHODI_Racuni
            #return self.ODHODI
        # spodnji elif sem vključil že zgoraj
        #elif VirDN=="Bar": #za Rez_DN_Bar vrni tabelo Stayover + Prihodi
        #    return ZDRprh_styov
        
        elif self.vir=="DNPOROCILA":
            pass
            #print(STAYOVER_MP)
        
        elif self.vir=="Bar": #za Rez_DN_Bar vrni tabelo Stayover + Prihodi
            return self.ZDRprh_styov
        
        elif self.vir == "MySq_Obdat":
            return self.ob_datum, self.T_SobeODH_STOW_MENJ, self.T_Prihodi1, self.T_Graf, self.T_PrazneSobe
        
    """





# prihodi s queryset- verjetno tega ne bom več rabil
    """def prihodi(self):
        self.prihodi_data = self.podatki.filter(od_dt=self.ob_datum)
        self.prihodi_data= self.prihodi_data.annotate(Status= Value('', output_field=models.CharField(max_length=20)))
        self.prihodi_data= self.prihodi_data.annotate(StatusCheckIn= Value('', output_field=models.CharField(max_length=20))) 
        self.prihodi_data= self.prihodi_data.annotate(cas_checkin= Value(datetime.now(), output_field=models.DateTimeField())) 
        
        # Rename filde, da bodo kompatibilni z appom: Aplikacija
        self.prihodi_data= (self.prihodi_data.annotate(Od = F("od")).annotate(Do = F("do")).annotate(Soba = F("stsobe"))
            .annotate(DatumVnosa = F("datumvnosa")).annotate(Ime = F("imestranke")).annotate(Agencija = F("agencija"))
            .annotate(Cena = F("CENA")).annotate(Tip = F("tip")).annotate(Drzava = F("DR")).annotate(Zahteve = F("zahteve"))
            .annotate(Ttax = F("StanjeTTAX")).annotate(St_Oseb = F("SO"))
            )
        #self.prihodi_data= self.prihodi_data
        #self.prihodi_data= self.prihodi_data
        #self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        # self.prihodi_data= self.prihodi_data
        self.prihodi_data= self.prihodi_data.values(
            "Soba", "St_Oseb", "DatumVnosa", "Ime", "Agencija", 
            "Od", "Do", "Cena", "Tip", "Drzava", "Zahteve", "Alergije", 
            "RNA", "Ttax", "Status", "StatusCheckIn", "cas_checkin", "st_noci")
        #print(self.prihodi_data)
        #for item in self.prihodi_data:
         #   vsebina = item.Status
          #  print(vsebina)
        

        return self.prihodi_data

        # dodaj stevilo noci (rabiš za vingcard)
"""

