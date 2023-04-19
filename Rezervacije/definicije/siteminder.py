import pandas as pd
import numpy as np

class Siteminder:
    def __init__(self, podatki, od_datum):
        self.podatki = podatki
        self.ob_datum= pd.to_datetime(od_datum, format="%d.%m.%Y")
        self. L_TipiSob=["c","s","q","d","f","g","x","y"]
        #print(self.podatki)
        self.podatki["datumvnosa"]=pd.to_datetime(self.podatki["datumvnosa"],format="%d.%m.%Y").dt.normalize()
        self.podatki["od"]=pd.to_datetime(self.podatki["od"],format="%d.%m.%Y").dt.normalize()
        self.podatki["do"]=pd.to_datetime(self.podatki["do"],format="%d.%m.%Y").dt.normalize()
    
    def obdelava_podatki_sm(self):
        #Pridobi število vrstic - potrebuješ za indeksiranje, ko boš z loopom iskal številko sobe
        St_vrsticArhiv=self.podatki.shape[0]
               
        #Naredi nov STOLPEC Št nočitev: Izračunaj število nočitev iz do-od
        self.podatki["St_Nocitev"]=(self.podatki["do"]-self.podatki["od"]).dt.days #.dt.days odstrani besedo days
        
        #Loop skozi tabelo - poberi naslednje podatke iz 
        #ŠT SOBE
        #OD
        #ŠT NOČITEV
        #TIP SOBE

        
        T_ObravnavaneRez=self.podatki[(self.podatki["od"]>=self.ob_datum- pd.Timedelta(days=20))]
        #10.4.21 bilo 20:
        T_ObravnavaneRez=T_ObravnavaneRez[(T_ObravnavaneRez["do"]<=self.ob_datum+ pd.Timedelta(days=300))] 
        
        #print(T_ObravnavaneRez.shape[0])
        #print(T_ObravnavaneRez.loc[:,["imestranke","od","do"]])
        

        St_vrsticArhiv=T_ObravnavaneRez.shape[0]
        
        #Naredi list datumov
        Dat_prvi=self.ob_datum-pd.Timedelta(days=20)
        
        L_Dat=[]
        for i in range(320): #10.4.21 bilo 40  ##50
            i_Datum=Dat_prvi+ pd.Timedelta(days=i)
            L_Dat.append(str(i_Datum.day)+"."+str(i_Datum.month))
            #L_Dat.append(str(i_Datum.day)+"."+str(i_Datum.month)+"."+str(i_Datum.year))
            

        
        L_DatDOD=L_Dat.copy()
        
        T_GrafNov = pd.DataFrame(columns=L_DatDOD, index= self.L_TipiSob)
        
        # Dodaj števila MAX razpoložljivih sob po tipih
        for tip in self.L_TipiSob:
            indexTipaVListuTipov= self.L_TipiSob.index(tip)
            for i in range(len(L_DatDOD)-1):
                if tip=="c":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=8
                elif tip=="f":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=2
                elif tip=="g":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=3
                #elif tip=="b":
                #    T_GrafNov.iat[indexTipaVListuTipov,i]=0
                elif tip=="s":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=1
                elif tip=="y":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=1
                elif tip=="d":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=1
                elif tip=="q":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=5
                elif tip=="x":
                    T_GrafNov.iat[indexTipaVListuTipov,i]=4
                    
        
        #print(T_GrafNov)

        
        # Dodaj dodatno vrstico datumov za QT
        #for i in range(len(L_Dat)):
        #    T_GrafNov.iat[0,i+1]=L_Dat[i]
        
        # Dodaj dodaten stolpec števil sob za QT
        #for i in range(len(L_TipiSob)):
        #    T_GrafNov.iat[i,0]=L_TipiSob[i]
        
        # ODSTRANI NAN
        T_GrafNov=T_GrafNov.iloc[:,np.r_[0,0:320]]
        T_GrafNov = T_GrafNov.fillna(0) #ostrani NaN in jih nadomesti s " "
        #print(T_GrafNov)
        
        


        #GLAVNI LOOP
        for rez in range(St_vrsticArhiv):
            # Iz Pandas tabele loop skozi vse rezervacije in vsaki rezervaciji
            # potegneš podatke o št sobe, Oddatum, št.nočitev, št oseb in tip sobe
            
            # Vrstica je vsaka rezervacija v pandas tabeli
            #vrstica=T_Arhiv.loc[rez,:]     # loc- jemlje zaporedje števil vrstic: 0,1,2,3,, 
            vrstica=T_ObravnavaneRez.iloc[rez,:]  
            
            #Potegni podatke o posamezni rezervaciji:
            St_sobe=vrstica["stsobe"]
            od_d=pd.to_datetime(vrstica["od"])
            St_Noc=int(vrstica["St_Nocitev"])
            
            # Kakšen je index-Datum v Grafu za datum OD_D
            # Preveriš, kateri indeks je v Listu Datumi
            #Index_Datum=L_Datumi.index(OD_D)
            Indeks=((self.ob_datum-od_d).days)
            #print(Indeks)
            
            Index_Datum=20-Indeks # 20 zato, da v tabelo postavi ob datum 20 mest desno od levega roba tabele!
            
            # Polni tabelo z podatki c, g, x, f, .....
            TIP_C=[20,21,30,31,32,36,46,50]
            TIP_S=[37]
            TIP_G=[10,11,12]
            TIP_Y=[51]
            TIP_X=[35,38,39,45]
            TIP_F=[34,43]
            TIP_D=[40]
            TIP_Q=[33,41,42,44,52]     

            St_sobe.astype(int)
            
            if St_sobe in TIP_C:
                TIP_Sobe="c"
            elif St_sobe in TIP_S:
                TIP_Sobe="s"
            elif St_sobe in TIP_G:
                TIP_Sobe="g"
            elif St_sobe in TIP_Y:
                TIP_Sobe="y"
            elif St_sobe in TIP_X:
                TIP_Sobe="x"
            elif St_sobe in TIP_F:
                TIP_Sobe="f"
            elif St_sobe in TIP_D:
                TIP_Sobe="d"
            elif St_sobe in TIP_Q:
                TIP_Sobe="q"
            
            Index_TIP_Sobe=self.L_TipiSob.index(TIP_Sobe)
            
            
            for i in range(St_Noc):
                # Najprej prepiši staro vrednost tega tipa sobe
                Vrednost=T_GrafNov.iloc[Index_TIP_Sobe,Index_Datum+i+1]
                # odštej 1 od stare vrednosti in dobiš novo vrednost
                T_GrafNov.iat[Index_TIP_Sobe,Index_Datum+i+1]=int(Vrednost)-1
                #print(T_GrafNov)     
    
        
        return T_GrafNov.iloc[:,21:35] # Vrni v Rez_SM tabelo
    




        


        