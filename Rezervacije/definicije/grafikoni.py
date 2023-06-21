import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import gridspec
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
from Rezervacije.models import *

from django.db.models import Q, Count, Sum

import base64
from io import BytesIO

class Grafikoni:
    def __init__(self):
        
        # queryset >> pandas
        queryset = VnosGostov.objects.filter(status_rez="rezervirano")
        data = list(queryset.values())
        self.podatki = pd.DataFrame.from_records(data=data)
        self.podatki["datumvnosa"]=pd.to_datetime(self.podatki["datumvnosa"],format="%d.%m.%Y").dt.normalize()
        self.podatki["od"]=pd.to_datetime(self.podatki["od"],format="%d.%m.%Y").dt.normalize()
        self.podatki["do"]=pd.to_datetime(self.podatki["do"],format="%d.%m.%Y").dt.normalize()
        self.podatki = self.podatki.sort_values(by= ["datumvnosa"], ascending=True)
        

    def Priprava_Podatkov(self, leto_primerjava):
        #self.PrimerjavaLeto= self.LE_leto.text()
        leto_letos = str(pd.to_datetime("today").year)
        self.leto_primerjava = int(leto_primerjava)            #str(int(LetoLETOS)-1)

        # Zaradi varnosti, pretori datume v Pandas datume
        self.podatki["datumvnosa"]=pd.to_datetime(self.podatki["datumvnosa"],format="%d.%m.%Y").dt.normalize()
        self.podatki["od"]=pd.to_datetime(self.podatki["od"],format="%d.%m.%Y").dt.normalize()
        self.podatki["do"]=pd.to_datetime(self.podatki["do"],format="%d.%m.%Y").dt.normalize()
        self.podatki = self.podatki.sort_values(by= ["datumvnosa"], ascending=True)
        #PODATKI LETOS
            # DO > 1.1.20??
        self.T_Podatki_LETOS=self.podatki[self.podatki["do"]>=pd.to_datetime("1.1." + leto_letos,format="%d.%m.%Y")] 
            # DO < 31.12.20??
        self.T_Podatki_LETOS=self.T_Podatki_LETOS[self.T_Podatki_LETOS["do"]<=pd.to_datetime("31.12." + leto_letos,format="%d.%m.%Y")] 

        #PODATKI LANI
            # DO > 1.1.20??-1
        self.T_Podatki_LANI=self.podatki[self.podatki["do"]>=pd.to_datetime("1.1." + str(self.leto_primerjava),format="%d.%m.%Y")] 
            # DO < 31.12.20??-1
        self.T_Podatki_LANI=self.T_Podatki_LANI[self.T_Podatki_LANI["do"]<=pd.to_datetime("31.12." + str(self.leto_primerjava),format="%d.%m.%Y")] 





    #______________________ ANALIZE LETOŠNJEGA LETA  ________________________________________________________________
        
            

            ##########################################################################
            ## Podatki za primerjavo rez. ? dni v preteklost >> za kdaj rezervirano ##
            ##########################################################################
    def Pod_AnalizaZadnjihXdni(self, StDni):
        # Zadnjih xx dni
        self.T_Zad_XX_Dni = self.podatki[self.podatki["datumvnosa"] >= \
                            (pd.to_datetime("today") - pd.Timedelta (days = StDni))] 
                # Izloči samo rezervacije, ki so za tekoče leto- ne upoštevaj rezerv. za naslednje leto:
        self.T_Zad_XX_Dni = self.T_Zad_XX_Dni[self.T_Zad_XX_Dni["do"]<= pd.to_datetime("31.12."+ \
                            str(pd.to_datetime("today").year), format=("%d.%m.%Y"))]
        
        # Odstrani vse rezervacije PRED danes.
        #print(self.T_Zad_XX_Dni)
        #self.T_Zad_XX_Dni = self.T_Zad_XX_Dni[self.T_Zad_XX_Dni["od"] >= (pd.to_datetime("today"))] 
        #print(self.T_Zad_XX_Dni)
        self.T_Zad_XX_Dni = ((self.T_Zad_XX_Dni.groupby([self.T_Zad_XX_Dni['do'].dt.year.rename('leto'), self.T_Zad_XX_Dni['do'].dt.month.rename('mesec')]).count()["CENA"]).to_frame(name="st_rez").reset_index())
        T_Mesci1_12 = pd.DataFrame({"mesec":pd.Series(range(1,13))}) 
        
        self.T_Zad_XX_Dni=pd.merge(self.T_Zad_XX_Dni , T_Mesci1_12 , how=("outer"))
        self.T_Zad_XX_Dni = self.T_Zad_XX_Dni.sort_values(by= ["mesec"], ascending=True)
        self.T_Zad_XX_Dni = self.T_Zad_XX_Dni.fillna(0) 
        
        StRez = self.T_Zad_XX_Dni["st_rez"].sum()
        
        self.STDNI = StDni
        #print(self.T_Zad_XX_Dni)
        self.GrafAnalizaZadnjihXXdni()
        
        # Vnesi skupno število rezervacij v izbranem obdobju v Label L_stRez
        


        # MATPLOTLIB_GRAF
        
    def GrafAnalizaZadnjihXXdni(self):
        # MATPLOTLIB_GRAF
        self.sc = MplCanvas(self, width=12, height=6, dpi=100)
        
        self.T_Zad_XX_Dni[["mesec","st_rez"]].plot(ax=self.sc.axes, 
        x="mesec", y=["st_rez"], label = ["Število rez"], 
        kind="bar", title="Število rezervacij v zadnjih " + str(self.STDNI) + " dneh",colormap="winter_r",
        grid="both" ,sort_columns=True, style="dark_background",
        fontsize=11, stacked = False, legend  = True,
        table = True
        )
        self.sc.axes.set_xticklabels(self.T_Zad_XX_Dni["mesec"].tolist(),rotation=30)
        #self.sc.axes.set_yticklabels(self.T_Zad_XX_Dni["st_rez"].tolist(),rotation=30)
        legend = self.sc.axes.legend(loc='upper right', shadow=True, fontsize='x-large')
        legend.get_frame().set_facecolor('C2')
        self.sc.axes.get_xaxis().set_visible(False)
        
        
        
        #self.Vertikalec = QVBoxLayout(self.WidgMatPlot)
        self.Vertikalec.addWidget(self.sc)


        #self.setCentralWidget(self.sc)
        #self.show()
        # 




    ##########################
    ## TREND REZERVACIJ ######
    ##########################
    # Podatki
    def Pod_TrendRezervacij(self, StDni): # Izračuna kolikšna je suma rezervacij zadnjih XXdni na posamezni dan
        #self.TrendRezervacij =  self.CELOTNIpodatki.groupby("datumvnosa").sum()["CENA"].to_frame(name="CENA").reset_index() 
        self.TrendRezervacij = self.podatki
        
        
        #self.TrendRezervacij["StNocitevSK"] = self.TrendRezervacij[(self.TrendRezervacij["SO"] * (self.TrendRezervacij["do"] - self.TrendRezervacij["od"]).dt.days)]
        self.TrendRezervacij["StDNI"]=(self.TrendRezervacij["do"]-self.TrendRezervacij["od"]).dt.days
        self.TrendRezervacij["StNocitevSK"] = self.TrendRezervacij["StDNI"] * self.TrendRezervacij["SO"] 
        
        self.TrendRezervacij = self.TrendRezervacij[self.TrendRezervacij["do"] <= pd.to_datetime(("31.12.") + str(pd.to_datetime("today").year), format= "%d.%m.%Y") ]
        
        self.TrendRezervacij = self.TrendRezervacij.groupby(["datumvnosa"],as_index=False).agg({"StNocitevSK": "sum", 'SO': 'sum','CENA': 'sum','StDNI': 'mean','agencija': 'count' })
                
        self.TrendRezervacij =  self.TrendRezervacij.iloc[-100:,:]   # pridobi zadnjih 100 rezervacij 
        self.TrendRezervacij = self.TrendRezervacij[["datumvnosa" , "CENA", "SO", "agencija", "StNocitevSK"]].reset_index(drop=True, inplace=False)
        
        # Seštevki na grafu Trend rez. : št oseb, št rezervacij, št nočitev
        self.TrendRezervacijA=self.TrendRezervacij.loc[self.TrendRezervacij['datumvnosa']>=(pd.to_datetime("today")- pd.Timedelta(days = StDni))]
        
        IndexSO = self.TrendRezervacijA.columns.get_loc("SO")
        SkupajGostov =  self.TrendRezervacijA.iloc[:,IndexSO].sum()
        IndexStRez = self.TrendRezervacijA.columns.get_loc("agencija")
        SkupajStRez = self.TrendRezervacijA.iloc[:,IndexStRez].sum()
        IndexStNoc = self.TrendRezervacijA.columns.get_loc("StNocitevSK")
        SkupajStNocitev = self.TrendRezervacijA.iloc[:,IndexStNoc].sum()

        # Vnesi podatke o št. gostov in št. rezervacj v graf
        self.L_StGostov.setText(str(SkupajGostov))
        self.L_StRezerv.setText(str(SkupajStRez))
        self.L_StNocitev.setText(str(SkupajStNocitev))

        
        #self.T_Zad_XX_Dni = ((self.T_Zad_XX_Dni.groupby([self.T_Zad_XX_Dni['do'].dt.year.rename('leto'), self.T_Zad_XX_Dni['do'].dt.month.rename('mesec')]).count()["CENA"]).to_frame(name="st_rez").reset_index())

        # ustvari prazno tabelo z datumi, in vanjo vnašaj sume cen po datumih - od spodnje strani tabele navzgor
        
        Datumi = pd.date_range(start= pd.to_datetime("today")- pd.Timedelta(days = 30), end= pd.to_datetime("today"),freq='d', normalize=True)
        self.Tabela = pd.DataFrame({"Datumi": Datumi , "Stolp2": 1})
        self.Tabela.set_index("Datumi")
        
        StVrstic = self.Tabela.shape[0]  # ugotovi, katera vrstica je zadnja

        while StVrstic > 0:
            #ZacetniDatum = self.Tabela.iloc[StVrstic-1, 0] 
            #print(ZacetniDatum)
            
            ZacetniDatum = self.Tabela.iloc[StVrstic-1, 0] - pd.Timedelta(days = StDni-1)  # zagrabi začetni datum OB. dneva
            KoncniDatum = self.Tabela.iloc[StVrstic-1, 0]
            
            # V tabeli s podatki naredi sumo med začetnim in končnim datumom
            T_rezultat = self.TrendRezervacij[self.TrendRezervacij["datumvnosa"]>= ZacetniDatum]
            T_rezultat = T_rezultat[T_rezultat["datumvnosa"]<= KoncniDatum]
            
            #print(T_rezultat)
            SumaXXvrstic = round(T_rezultat["CENA"].sum(),2)
            
            # Vnesi sumo zadnjih 7 dni rezervacij na obravnavani dan
            self.Tabela.iat[StVrstic-1, 1] = SumaXXvrstic 
            # V stolpec Datum vnesi datum v obliki: 5.6
            self.Tabela.iat[StVrstic-1, 0] = str(KoncniDatum.day) + "." + str(KoncniDatum.month)
            
            
            StVrstic -= 1 
        
        self.Graf_Trend_rezervacij()

    def Graf_Trend_rezervacij(self):
        
        

        # MATPLOTLIB_GRAF
        self.sc = MplCanvas(self, width=12, height=6, dpi=100)
        
        self.Tabela[["Datumi","Stolp2"]].plot(ax=self.sc.axes, 
        x="Datumi", y=["Stolp2"], label = ["EUR"], 
        kind="bar", title="Trend 7 dnevnih VSOT prihodkov",colormap="winter_r",
        grid="both" ,sort_columns=True, style="dark_background",
        fontsize=11, stacked = False, legend  = True,
        table = True
        
        )
        """
        xx= self.Tabela["Datumi"]       
        self.sc.axes.set_xticks(xx)
        self.sc.axes.set_xticklabels([i for i in xx]) #, rotation=0)
        """
        
        legend = self.sc.axes.legend(loc='upper left', shadow=True, fontsize='x-large')
        legend.get_frame().set_facecolor('C2')
        self.sc.axes.get_xaxis().set_visible(False)
        
        









    #______________________ PRIMERJAVE S PREJŠNJIMI LETI ________________________________________________________________


    ########################      
    # Podatki za agencije ##
    ########################

    def Pod_Agencije(self):
        # LETOS
            # Pretvori Groupby rezultat v DATAFRAME, da ga lahko obdeluješ        
        self.Priprava_Podatkov()
        T_ProfitAG_LETOS=self.T_Podatki_LETOS.groupby("agencija").sum()["CENA"].to_frame(name="CenaLetos").reset_index() #!!!!!!
        T_ProfitAG_LETOS["CenaLetos"]=T_ProfitAG_LETOS["CenaLetos"].round(2)
        T_ProfitAG_LETOS=T_ProfitAG_LETOS.sort_values(by=['CenaLetos'], ascending = False)

        Agencije =  T_ProfitAG_LETOS["agencija"].tolist()
        EUR = T_ProfitAG_LETOS["CenaLetos"].tolist()
        T_Agencije_Letos=T_ProfitAG_LETOS["agencija"]
        #print(T_ProfitAG_LETOS)

            # LANI
            # Pretvori Groupby rezultat v DATAFRAME, da ga lahko obdeluješ        
        T_ProfitAG_LANI=self.T_Podatki_LANI.groupby("agencija").sum()["CENA"].to_frame(name="CenaLani").reset_index() #!!!!!!
        T_ProfitAG_LANI["CenaLani"]=T_ProfitAG_LANI["CenaLani"].round(2)
        T_ProfitAG_LANI=T_ProfitAG_LANI.sort_values(by=['CenaLani'], ascending = False)

        Agencije =  T_ProfitAG_LANI["agencija"].tolist()
        EUR = T_ProfitAG_LANI["CenaLani"].tolist()
        T_Agencije_Lani=T_ProfitAG_LETOS["agencija"]
        #print(T_ProfitAG_LANI)


        self.T_Zdruzena= pd.merge(T_ProfitAG_LANI,T_ProfitAG_LETOS, how="outer")
        self.T_Zdruzena= self.T_Zdruzena.fillna(0)

        self.Agencije_Graf()


    def Agencije_Graf(self):
        
        self.sc = MplCanvas(self, width=16, height=8, dpi=100)
        
        
        
        self.T_Zdruzena[["agencija","CenaLani","CenaLetos"]].plot(ax=self.sc.axes, 
                        x="agencija", y=["CenaLani","CenaLetos"], 
                        label = [self.leto_primerjava, "Letos"], kind="bar", title="Prihodki po agencijah",
                        colormap="winter_r", grid="both", sort_columns=True, 
                        style="dark_background", fontsize=10, table=True)
        
        self.sc.axes.set_xticklabels(self.T_Zdruzena["agencija"].tolist(), rotation=30)
        legend = self.sc.axes.legend(loc='upper center', shadow=True, fontsize='x-large')
        legend.get_frame().set_facecolor('C2')
        self.sc.axes.get_xaxis().set_visible(False)

        self.Vertikalec.addWidget(self.sc)



        #############################
        # Podatki za EUR po mescih ##
        #############################
    def Pod_EUR_po_Mescih(self):
        self.Priprava_Podatkov()
        T_EUR_PoMescih_Lani=self.T_Podatki_LANI[["do","CENA"]]
        T_EUR_PoMescih_Lani=((self.T_Podatki_LANI.groupby([self.T_Podatki_LANI['do'].dt.year.rename('letoLani'), self.T_Podatki_LANI['do'].dt.month.rename('mesec')]).sum()["CENA"]).to_frame(name="CenaLani").reset_index()) # !!!!!!
        T_EUR_PoMescih_Lani = T_EUR_PoMescih_Lani.astype(int)
        
        T_EUR_PoMescih_Letos=self.T_Podatki_LETOS[["do","CENA"]]
        T_EUR_PoMescih_Letos=((self.T_Podatki_LETOS.groupby([self.T_Podatki_LETOS['do'].dt.year.rename('letoLetos'), self.T_Podatki_LETOS['do'].dt.month.rename('mesec')]).sum()["CENA"]).to_frame(name="CenaLetos").reset_index()) # !!!!!!
        T_EUR_PoMescih_Letos = T_EUR_PoMescih_Letos.astype(int)
        
        T_Mesci1_12 = pd.DataFrame({"mesec":pd.Series(range(1,13))})   # !!!!!
        
        T_EUR_Lani_Zdruzena= pd.merge(T_Mesci1_12,T_EUR_PoMescih_Lani, how="outer")
        T_EUR_Lani_Zdruzena=T_EUR_Lani_Zdruzena.sort_values(by=['mesec'], ascending = True)
        
        self.T_EUR_Lani_Zdruzena= pd.merge(T_EUR_Lani_Zdruzena,T_EUR_PoMescih_Letos, how="outer")
        
        self.T_EUR_Lani_Zdruzena= self.T_EUR_Lani_Zdruzena.fillna(0)
        #print(self.T_EUR_Lani_Zdruzena)

        self.PoMescih_Graf()

    def PoMescih_Graf(self):
        # MATPLOTLIB_GRAF
        self.brisanjeLayouta()
        self.L_stReze.setText("")
        self.L_kum_lani.setText("")
        self.L_kum_letos.setText("")
        self.L_StGostov.setText("")
        self.L_razlika.setText("")
        self.L_StNocitev.setText("")
        self.L_StRezerv.setText("")
        

        self.sc = MplCanvas(self, width=12, height=6, dpi=100)
        

        self.T_EUR_Lani_Zdruzena[["mesec","CenaLani","CenaLetos"]].plot(ax=self.sc.axes, 
        x="mesec", y=["CenaLani","CenaLetos"], label = [self.leto_primerjava, "Letos"], 
        kind="bar", title="Prihodki EUR",colormap="winter_r",
        grid="both" ,sort_columns=True, style="dark_background",
        fontsize=11, stacked = False, legend  = True,
        table = True
        
        )
        
        self.sc.axes.set_xticklabels(self.T_EUR_Lani_Zdruzena["mesec"].tolist(),rotation=30)
        legend = self.sc.axes.legend(loc='upper right', shadow=True, fontsize='x-large')
        legend.get_frame().set_facecolor('C2')
        self.sc.axes.get_xaxis().set_visible(False)
        
        
        self.Vertikalec.addWidget(self.sc)


        ###################################################################
        ##  Podatki za primerjavo kumulative do današnjega dne ##
        ###################################################################
    def Pod_Kumulativa_DoDanes(self, leto_primerjava):
        self.LetoLetos = pd.to_datetime("today").year
        self.leto_primerjava = int(leto_primerjava)   #int(self.LE_leto.text())
        T_Kumul_Do_DanDneLANI = self.podatki[self.podatki["do"]>= pd.to_datetime("1.1." + str(self.leto_primerjava))]
        T_Kumul_Do_DanDneLANI = T_Kumul_Do_DanDneLANI[T_Kumul_Do_DanDneLANI["do"]<= pd.to_datetime("31.12." + str(self.leto_primerjava))]   #str(pd.to_datetime("today").year - 1))]
        
        T_Kumul_Do_DanDneLANI = T_Kumul_Do_DanDneLANI[T_Kumul_Do_DanDneLANI["datumvnosa"] <= 
                    (pd.to_datetime("today") - pd.Timedelta(days = (self.LetoLetos - self.leto_primerjava) * 365))] 
        

        T_Kumul_DoDanDneLETOS = self.podatki[self.podatki["do"]>= pd.to_datetime("1.1." + str(pd.to_datetime("today").year))]
        T_Kumul_DoDanDneLETOS = T_Kumul_DoDanDneLETOS[T_Kumul_DoDanDneLETOS["do"]<= pd.to_datetime("31.12." + str(pd.to_datetime("today").year))]
        self.T_Kumul_DoDanDneLETOS = T_Kumul_DoDanDneLETOS[T_Kumul_DoDanDneLETOS["datumvnosa"] <= (pd.to_datetime("today"))] 
        #print(f"(Kumul {T_Kumu_DoDanDneLETOS}")

        #T_EUR_PoMescih_Letos = T_EUR_PoMescih_Letos.astype(int)
        Suma_LANI = T_Kumul_Do_DanDneLANI["CENA"].sum()
        
        Suma_LETOS = T_Kumul_DoDanDneLETOS["CENA"].sum()
        
        # Vnesi sumo kumulativ za lani in za letos v L_kum_lani / letos
        


        ###################################################################
        ## Podatki za primerjavo kumulative do današnjega dne PO MESECIH ##
        ###################################################################
        # LANI
        #print(T_Kumul_Do_DanDneLANI["CENA"])
        T_Kumul_Do_DanDneLANI=((T_Kumul_Do_DanDneLANI.groupby([T_Kumul_Do_DanDneLANI['do'].dt.year.rename('letoLani'), T_Kumul_Do_DanDneLANI['do'].dt.month.rename('mesec')])["CENA"].sum()).to_frame(name="CenaLani").reset_index())

        


        T_Kumul_Do_DanDneLANI = T_Kumul_Do_DanDneLANI.astype(int)
        print(T_Kumul_Do_DanDneLANI)

        # LETOS
        T_Kumul_DoDanDneLETOS=((T_Kumul_DoDanDneLETOS.groupby([T_Kumul_DoDanDneLETOS['do'].dt.year.rename('letoLetos'), T_Kumul_DoDanDneLETOS['do'].dt.month.rename('mesec')])["CENA"].sum()).to_frame(name="CenaLetos").reset_index())
        T_Kumul_DoDanDneLETOS = T_Kumul_DoDanDneLETOS.astype(int)
        #print(T_Kumul_DoDanDneLETOS)


        T_Mesci1_12 = pd.DataFrame({"mesec":pd.Series(range(1,13))})   # !!!!!

        T_Kumul_Zdruzena_Lani_Letos = pd.merge(T_Mesci1_12, T_Kumul_Do_DanDneLANI, how=("outer"))
        T_Kumul_Zdruzena_Lani_Letos=T_Kumul_Zdruzena_Lani_Letos.sort_values(by=['mesec'], ascending = True)
        T_Kumul_Zdruzena_Lani_Letos = pd.merge(T_Kumul_Zdruzena_Lani_Letos, T_Kumul_DoDanDneLETOS, how=("outer"))
        self.T_Kumul_Zdruzena_Lani_Letos = T_Kumul_Zdruzena_Lani_Letos.fillna(0) 
        #print(self.T_Kumul_Zdruzena_Lani_Letos)


        # MATPLOT

        # Create a figure and axis objects
        fig, (ax1) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

        # Set the bar width
        bar_width = 0.35

        mesci = self.T_Kumul_Zdruzena_Lani_Letos['mesec']
        
        # Calculate the positions of the bars on the x-axis
        
        x = np.arange(len(mesci))
        y = self.T_Kumul_Zdruzena_Lani_Letos['CenaLani']
        y1 = self.T_Kumul_Zdruzena_Lani_Letos['CenaLetos']


        # Create the figure and grid layout
        fig = plt.figure(figsize=(15, 8))  # Increase the figsize
        grid = fig.add_gridspec(2, 1, height_ratios=[3, 1])

        # Create the bar chart in the first grid
        ax1 = fig.add_subplot(grid[0, 0])
        ax1.bar(x, y, bar_width, label= self.leto_primerjava)
        ax1.bar(x + bar_width, y1, bar_width, label=pd.to_datetime("today").date().year)

        # Set labels, title, and legend for the chart
        ax1.set_xlabel('Mesec')
        ax1.set_ylabel('EUR')
        ax1.set_title('Kumulativa do danes')
        ax1.set_xticks(x + bar_width / 2)
        ax1.set_xticklabels(mesci)
        ax1.legend()
        ax1.table(cellText=self.T_Kumul_Zdruzena_Lani_Letos[["mesec","CenaLani","CenaLetos"]].T.values,
                  rowLabels=["mesec", self.leto_primerjava, pd.to_datetime("today").date().year], bbox=[0, -0.35, 1, 0.2]),  # Adjust the position and size of the table)
                    

   

        # Save the plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_image = base64.b64encode(buffer.getvalue()).decode()

      
       
        return plot_image
       
       
       
        #canvas = FigureCanvas(fig)
        #return canvas
        #response = HttpResponse(content_type='image/png')
        #canvas.print_png(response)

        #return response















        # # MATPLOTLIB_GRAF
        # self.sc = MplCanvas(self, width=12, height=6, dpi=100)
        

        # self.T_Kumul_Zdruzena_Lani_Letos[["mesec","CenaLani","CenaLetos"]].plot(ax=self.sc.axes, 
        # x="mesec", y=["CenaLani","CenaLetos"], label = [self.leto_primerjava, "Letos"], 
        # kind="bar", title="DoDanes EUR",colormap="winter_r",
        # grid="both" ,sort_columns=True, style="dark_background",
        # fontsize=11, stacked = False, legend  = True,
        # table = True
        
        # )
        
        # self.sc.axes.set_xticklabels(self.T_Kumul_Zdruzena_Lani_Letos["mesec"].tolist(),rotation=30)
        # legend = self.sc.axes.legend(loc='upper right', shadow=True, fontsize='x-large')
        # legend.get_frame().set_facecolor('C2')
        # self.sc.axes.get_xaxis().set_visible(False)
        
        

