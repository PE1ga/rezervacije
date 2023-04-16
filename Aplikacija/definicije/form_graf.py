import pandas as pd
#from openpyxl.workbook import Workbook
#from openpyxl import load_workbook
#import openpyxl
#from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
import sqlite3
import datetime as dt
#from datetime import datetime
#from datetime import timedelta
#from sqlalchemy import create_engine


def IzdelavaGrafa(DatumObravnave,Vir): #, DatumPrimerjave):
    #global T_ObravnavaneRez        
    #Določi List sob in jih napolni s številkami sob, ki jih dobiš iz tabele T_Graf 
    #L_Sobe=["xxx",10,11,12,20,21,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,50,51,52,99]
    #L_Sobe=["xxx","Dan",10,11,12,35,37,20,21,30,31,32,36,50,34,43,38,39,45,51,40,33,41,42,44,52,99,"Profit","Zajtrki","Menjave","StSOB","Prihodi"]
    L_Sobe=["xxx","Dan",10,11,12,37,20,21,30,31,32,36,50,34,43,35,38,39,45,51,40,33,41,42,44,52,99,"Profit","Zajtrki","Menjave","StSOB","Prihodi"]
    
    # NALOŽI PODATKE IZ SQL
    #Pridobi tabelo ArhivGostov iz SQL
    con = sqlite3.connect('C:/DjRezerv/MojProjekt/db.sqlite3')
    T_Arhiv = pd.read_sql_query("SELECT * FROM Aplikacija_vnosgostov", con)
   
    # Pretvori datume iz sql v pandas datume
        
    # Iz Pandas arraya pretvori datumske stolpce v pandas datum, tako, da pandasu poveš, kakšen je format datumov v SQL (d.m.Y)
    T_Arhiv["datumvnosa"]=pd.to_datetime(T_Arhiv["datumvnosa"],format="%d.%m.%Y")
    T_Arhiv["od"]=pd.to_datetime(T_Arhiv["od"],format="%d.%m.%Y") # Definiraš, v kakšenm formatu so datumi prišli iz SQL 
    T_Arhiv["do"]=pd.to_datetime(T_Arhiv["do"],format="%d.%m.%Y")
    T_Arhiv['id'] = T_Arhiv['id'].apply(str)
    # Arhiv gostov naj ima samo rezervacije, ki so bile pred DatumPrimerjave 
    
    """
    if DatumPrimerjave =="NiDefiniran":
        DatumPrimerjave = datetime.strptime("31.12.2100","%d.%m.%Y")

    T_Arhiv = T_Arhiv[T_Arhiv["datumvnosa"] <= DatumPrimerjave]
    """
    
    #T_Arhiv.info()
    
    #Pridobi število vrstic - potrebuješ za indeksiranje, ko boš z loopom iskal številko sobe
    St_vrsticArhiv=T_Arhiv.shape[0]
    #print(St_vrsticArhiv)

       
    #Naredi nov STOLPEC Št nočitev: Izračunaj število nočitev iz do-od
    T_Arhiv["St_Nocitev"]=(T_Arhiv["do"]-T_Arhiv["od"]).dt.days #.dt.days odstrani besedo days
    #print((T_Arhiv["St_Nocitev"]).head(30))   

    
    #Loop skozi tabelo - poberi naslednje podatke iz 
    #ŠT SOBE
    #OD
    #ŠT NOČITEV
    #TIP SOBE

    # Od OBDatuma pridobi rezervacije, ki imajo "OD" 20 dni pred OBDatum in ki imajo datum DO 20 dni po OBDatum
    
    
    #print(DatumObravnave)
    #OBDatum=dt.datetime.strptime(DatumObravnave,"%d.%m.%Y")
    OBDatum=DatumObravnave
    
    
    # Razlika med Obdatum in DanesDat >> Pomembno za barvanje današnjega datuma v rez_Optimiz
    RazlikaObdat_Danes=(OBDatum-pd.to_datetime("today")).days
    #print(RazlikaObdat_Danes)

    StDniPredINPo=50 # Število dni, kjer zajame rezervacije pred obravnavanim dnem in po obravnavenem dnevu. 
    #Zato, da so v obravnavanem datumu vidne in zajte vse rezervacije- še posebej je nevarno, da se ne bi pojavile dolge rezervacije
    # zato zaradi varnosti +-50 dni
    T_ObravnavaneRez=T_Arhiv[(T_Arhiv["od"]>=OBDatum-dt.timedelta(days=StDniPredINPo))]
    
    T_ObravnavaneRez=T_ObravnavaneRez[(T_ObravnavaneRez["do"]<=OBDatum+dt.timedelta(days=50))] 
    #print(T_ObravnavaneRez.dtypes)
    #print(T_ObravnavaneRez.shape[0])
    #print(T_ObravnavaneRez.loc[:,["imestranke","od","do"]])
    

    St_vrsticArhiv=T_ObravnavaneRez.shape[0]
    
    #Naredi list datumov
    Dat_prvi=OBDatum-dt.timedelta(days=StDniPredINPo)
    Dat_zadnji=OBDatum+dt.timedelta(days=StDniPredINPo)  #10.4.21 bilo 20 ##30
    #L_Dat=pd.date_range(Dat_prvi,Dat_zadnji,freq="d")
    L_Dat=[]
    for i in range(StDniPredINPo*2): #10.4.21 bilo 40  ##50
        i_Datum=Dat_prvi+dt.timedelta(days=i)
        L_Dat.append(str(i_Datum.day)+"."+str(i_Datum.month)+".")
        #L_Dat.append(str(i_Datum.day)+"."+str(i_Datum.month)+"."+str(i_Datum.year))
        
    
    #Izdelaj Range of dates
    
    T_DatumiODDO=pd.date_range(start=Dat_prvi,end=Dat_zadnji).to_series()
    L_DatumiODDO=(T_DatumiODDO.dt.day_name(locale="English")).tolist() #!!!!! ime dneva v tednu 
    #print(L_DatumiODDO)
    L_SloDnevi=[]
    #for index,dan in enumerate(L_DatumiODDO):
    for dan in enumerate(L_DatumiODDO):
        if dan[1]=="Monday":
            L_SloDnevi.append("pon")
        elif dan[1]=="Tuesday":
            L_SloDnevi.append("tor")
        elif dan[1]=="Wednesday":
            L_SloDnevi.append("sre")
        elif dan[1]=="Thursday":
            L_SloDnevi.append("čet")
        elif dan[1]=="Friday":
            L_SloDnevi.append("pet")
        elif dan[1]=="Saturday":
            L_SloDnevi.append("sob")
        elif dan[1]=="Sunday":
            L_SloDnevi.append("ned")
        
    

    L_DatDOD=L_Dat.copy()
    L_DatDOD.insert(0,"Sobe")
   

    #####################################
    #### Izdelaj PRAZNO pandas tabelo ###
    #####################################

    # - imena stolpcev so datumi, indexi so št sob 
        
    #T_GrafNov = pd.DataFrame(columns=L_DatDOD, index=L_Sobe)
    T_GrafNov = pd.DataFrame(columns=L_DatDOD, index=L_Sobe)
    
    # Dodaj dodatno vrstico datumov za QT
    for i in range(len(L_Dat)):
        T_GrafNov.iat[0,i+1]=L_Dat[i]
    
    # Na mesto današnjega datuma dodaj ..
    if RazlikaObdat_Danes>=-20 and RazlikaObdat_Danes<=20:
        #T_GrafNov.iat[0,StDniPredINPo-RazlikaObdat_Danes]=T_GrafNov.iat[0,StDniPredINPo-RazlikaObdat_Danes]+"_"
        T_GrafNov.iat[0,StDniPredINPo-RazlikaObdat_Danes]="DNS"





    # Dodaj imena dnevov v vrstico pod datumi
    for i in range(len(L_SloDnevi)-1):
        T_GrafNov.iat[1,i+1]=L_SloDnevi[i]
    


    # Dodaj dodaten stolpec števil sob za QT
    for i in range(len(L_Sobe)):
        T_GrafNov.iat[i,0]=L_Sobe[i]
    
    #####################################################
    ### KOPIJE PRAZNE TABELE - ZA IZRAČUN CEN PO DNEVIH##
    ######################################################
    T_Graf_CENE=T_GrafNov.copy()    #potrebujem za izračun cen
    T_Graf_ZAJTRKI=T_GrafNov.copy()    #potrebujem za izračun števila zajtrkov po dnevih
    T_Graf_MENJAVE=T_GrafNov.copy()

    T_Graf_STSOB=T_GrafNov.copy()
    T_Graf_PRIHOD=T_GrafNov.copy()

    
    #####################################################
    ##########################
    ######  GLAVNI LOOP   ####
    ##########################
    #####################################################
    for rez in range(St_vrsticArhiv):
        # Iz Pandas tabele loop skozi vse rezervacije in vsaki rezervaciji
        # potegneš podatke o št sobe, Oddatum, št.nočitev, št oseb in tip sobe
        
        # Vrstica je vsaka rezervacija v pandas tabeli
        #vrstica=T_Arhiv.loc[rez,:]     # loc- jemlje zaporedje števil vrstic: 0,1,2,3,, 
        vrstica=T_ObravnavaneRez.iloc[rez,:]  #iloc - jemlje indeks vrstic v tabeli. (prvi vnos je lahko vrstica 255, zato loc ne deluje!!!!!)
        
        #Potegni podatke o posamezni rezervaciji:
        IndeksVrstice = vrstica["id"]
        St_sobe=vrstica["stsobe"]
        Ime = vrstica["imestranke"]
        OD_D=pd.to_datetime(vrstica["od"])
        St_Noc=int(vrstica["St_Nocitev"])
        St_oseb=str(vrstica["SO"])
        Tip_sobe=vrstica["tip"]
        UNIkod=vrstica["sifravnosa"]
        CenaSK=vrstica["CENA"]
        AgencijA=vrstica["agencija"]
        CenaNaNoc=CenaSK/St_Noc
        ZaklenjenaSoba=vrstica["Zaklenjena"] # za rezervacije, ki hočejo to sobo
        
      
        # Kakšen je index-Datum v Grafu za datum OD_D
        # Preveriš, kateri indeks je v Listu Datumi
        #Index_Datum=L_Datumi.index(OD_D)
        Indeks=((OBDatum-OD_D).days)
        #print(Indeks)
        
        Index_Datum=50-Indeks
        #print("Stolp: "+str(Index_Datum))  # stolpci
        
        
        # Kakšen je index za Št Sobe
        # Preveriš, kateri indeks je v Listu Sobe
        #print("Št sobe: "+ str(St_sobe))
        
        Index_St_Sobe=L_Sobe.index(St_sobe)
        
        # Polni tabelo s podatki c, g, x, f, .....
        
        for i in range(St_Noc):
            if Vir=="DN":   #Če je zahteva prišla od modula Rez_DN. oz Rez_Vnos, oz Rez_Ponudba..
                # Vnesi cenonanoč za vsako sobo v vsak dan v tabelo
                T_Graf_CENE.iat[Index_St_Sobe,Index_Datum+i+1]=float(CenaNaNoc)
                # Vnesi zajtrk za vsako sobo v vsak dan v tabelo
                T_Graf_ZAJTRKI.iat[Index_St_Sobe,Index_Datum+i+1]=int(St_oseb)
                # Vnesi menjave za vsako sobo v vsak dan v tabelo
                if i==St_Noc-1:
                    T_Graf_MENJAVE.iat[Index_St_Sobe,Index_Datum+i+1]=1

                # Vnesi Število vseh sob v vsak dan v tabelo, tako, da dodaš 1
                T_Graf_STSOB.iat[Index_St_Sobe,Index_Datum+i+1]=1

                #Pridobi tabelo, s številom prihodov
                if i==0:
                    T_Graf_PRIHOD.iat[Index_St_Sobe,Index_Datum+i+1]=1
                
                
                
                
                # vnesi v tablo T_graf-nov: c2>,...
                if i==St_Noc-1:
                    T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=Tip_sobe+St_oseb+">"     # ROW,COLUMN
                else:
                    T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=Tip_sobe+St_oseb
                
                # Če je Soba zaklenjena>> dodaj piko, da se na excel grafu vidi, da gre za zaklenjeno sobo 
                if ZaklenjenaSoba=="Zaklenjena":
                    T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]+"."
                    


                
            # Poizvedba za število zajtrkov
            elif Vir=="DN_zajtrki":
                T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=int(St_oseb)

            # Poizvedba za profit po dnevih
            elif Vir=="DN_ProfitPoDnevih":
                T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=float(CenaNaNoc)


            # Poizvedba za število menjav
            elif Vir=="DN_menjave":
                if i==St_Noc-1:
                    T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=1


            # To poročilo gre v REZ OPTIM- posreduješ prvo celico z UNIKODO+agencijo+ZAKLENJENO___ Agencijo dodaš zato, da se v Optim uporabi opcija barvanja celic glede na agencijo
            # V Rez_Optim se uni koda izloči tako, da program prebere prvih 13 znakov iz te celice.
            
            elif Vir=="R_Optimi":
            
            #else:     
                if i==0:
                    if St_Noc == 1:
                        T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]= IndeksVrstice  + "_:" +Ime +" "+ Tip_sobe + St_oseb + " " + AgencijA + " " + ">"
                    else:
                        T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]= IndeksVrstice  + "_:" +Ime +" "+ Tip_sobe + St_oseb + " " + AgencijA 
                   

                elif i==St_Noc-1:
                    T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=Tip_sobe+St_oseb+">"     # ROW,COLUMN
                else:
                    T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]=Tip_sobe+St_oseb
                
                # Vnesi cenonanoč za vsako sobo v vsak dan v tabelo
                T_Graf_CENE.iat[Index_St_Sobe,Index_Datum+i+1]=float(CenaNaNoc)
                # Vnesi cenonanoč za vsako sobo v vsak dan v tabelo
                T_Graf_ZAJTRKI.iat[Index_St_Sobe,Index_Datum+i+1]=int(St_oseb)
                # Vnesi menjave za vsako sobo v vsak dan v tabelo
                if i==St_Noc-1:
                    T_Graf_MENJAVE.iat[Index_St_Sobe,Index_Datum+i+1]=1
                
                # Vnesi Število vseh sob v vsak dan v tabelo, tako, da dodaš 1
                T_Graf_STSOB.iat[Index_St_Sobe,Index_Datum+i+1]=1
            
                #Pridobi tabelo, s številom prihodov
                if i==0:
                    T_Graf_PRIHOD.iat[Index_St_Sobe,Index_Datum+i+1]=1
            
            elif Vir=="R_Optimi_iskanjeRez":
                if i==0:
                    T_GrafNov.iat[Index_St_Sobe,Index_Datum+i+1]= IndeksVrstice

    
    # PODATKI ZA GRAF V excel tabeli GRAF
    if Vir=="DN" or Vir=="R_Optimi":
        collist=list(T_GrafNov) # IZDELA LIST IMEN STOLPCEV !!!!!!
        del collist[0]      # ODSTRANIŠ ELEMENTE IZ LISTA GLEDE NA INDEX !!!!!
        del collist[0]
        
        # PROFIT
        # Vrstice S SUMAMI zajtrki, prihodek,....
        # Napolniš List L_Sume s sumami po dnevih
        L_Sume=[]
        for i in collist:
            suma=(T_Graf_CENE.iloc[2:][i].sum(axis = 0, skipna = True)) # SEŠTEVANJE PO STOLPCIH + ODSTANI NAN  !!!!!
            L_Sume.append(suma)
        # dodaj list suma v T_Graf_nov
        for j in range(len(L_Sume)-1):
            T_GrafNov.iat[-5,3+j]=L_Sume[j]  # -2,-3.. , ker je na predzadnji poziciji v tabeli (predzadnja vrstica)
        
        # ZAJTRKI
        # Napolniš List L_Sume s sumami zajtrkov po dnevih
        L_Sume=[]
        for i in collist:
            suma=(T_Graf_ZAJTRKI.iloc[2:][i].sum(axis = 0, skipna = True)) # SEŠTEVANJE PO STOLPCIH + ODSTANI NAN
            L_Sume.append(suma)
        # dodaj list suma v T_Graf_nov
        for j in range(len(L_Sume)-1):
            T_GrafNov.iat[-4,3+j]=L_Sume[j]
        
        # MENJAVE
        # Napolniš List L_Sume s sumami zajtrkov po dnevih
        L_Sume=[]
        for i in collist:
            suma=(T_Graf_MENJAVE.iloc[2:][i].sum(axis = 0, skipna = True)) # SEŠTEVANJE PO STOLPCIH + ODSTANI NAN
            L_Sume.append(suma)
        # dodaj list suma v T_Graf_nov
        for j in range(len(L_Sume)-1):
            T_GrafNov.iat[-3,3+j]=L_Sume[j]
        
        
        # ŠTEVILO VSEH SOB PO DNEVIH
       
        L_Sume=[]
        for i in collist:
            suma=(T_Graf_STSOB.iloc[2:][i].sum(axis = 0, skipna = True)) # SEŠTEVANJE PO STOLPCIH + ODSTANI NAN
            L_Sume.append(suma)
        # dodaj list suma v T_Graf_nov
        for j in range(len(L_Sume)-1):
            T_GrafNov.iat[-2,3+j]=L_Sume[j]
        
        # ŠTEVILO PRIHODOV PO DNEVIH
        L_Sume=[]
        for i in collist:
            suma=(T_Graf_PRIHOD.iloc[2:][i].sum(axis = 0, skipna = True)) # SEŠTEVANJE PO STOLPCIH + ODSTANI NAN
            L_Sume.append(suma)
        del L_Sume[0]
        # dodaj list suma v T_Graf_nov
        for j in range(len(L_Sume)-1):
            T_GrafNov.iat[-1,3+j]=L_Sume[j]
        


    #print(T_GrafNov.iloc[:,30:40])
    
    """
    # Prenos iz PANDAS v SQL tabelo (potrebuješ sqlalchemy in create_engine)
    engine=create_engine("sqlite:///DataBaza.db",echo=False)
    sqlite_povezava=engine.connect()
    sql_tabela="TabelaTest"
    T_GrafNov.to_sql(sql_tabela,sqlite_povezava,if_exists="replace")
    sqlite_povezava.close()
    """
    
    # v Rez_vnos.py returnaj tabelo z razpoložljivimi sobami
    #print(T_GrafNov)
    
    
    # priprava za DJANGO
    ListVrstice = [i for i in range(30)]
    ListStolpi = ["S" + str(i) for i in range(28)]
    T_Graf = pd.DataFrame(index=ListVrstice ,columns=ListStolpi)
    T_Graf.iloc[0:26,0] = T_GrafNov.iloc[0:26,0]
    T_Graf.iloc[0:26,1:28] = T_GrafNov.iloc[0:26,36:63]        #T_GrafNov.iloc[0:26,20:47]
    T_Graf.iloc[26:30,1:28] = T_GrafNov.iloc[28:32,36:63]
    T_Graf=T_Graf.fillna("")
    T_Graf.iat[26,0] = "Zaj"
    T_Graf.iat[27,0] = "Men"
    T_Graf.iat[28,0] = "StS"
    T_Graf.iat[29,0] = "Prh"
    
    # PRENESI V SQLITE
     # GRAF
    db=sqlite3.connect("C:/DjRezerv/MojProjekt/db.sqlite3")
    #db=sqlite3.connect("C:/DjRezerv/MojProjekt/db.sqlite3")
    kurzor = db.cursor()
    
    komanda = "DELETE FROM Aplikacija_graf ;"
    kurzor.execute(komanda)
    db.commit()
    T_Graf.to_sql('Aplikacija_graf', db, if_exists='append', index=False)

    kurzor.close()
    db.close()
    
    
    
    
    
    return T_Graf

    

def T_Rezervacije_OBtermin():
    pass
    #return T_ObravnavaneRez




       


   
#Zaženi
if __name__==("__main__"):
    print(IzdelavaGrafa(pd.to_datetime("20.7.2021",format=("%d.%m.%Y")),"R_Optimi"))  #"R_Optimi"))   "DN")) R_Optimi_iskanjeRez
    