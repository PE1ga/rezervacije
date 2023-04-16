#PROGRAM ZA ISKANJE PROSTIH SOB NEKEGA TIPA V DOLOČENEM TERMINU
import pandas as pd
import sqlite3
T_Data_Sobe = ""
T_izbraniP = ""

def PripravaPodatkov():
    
    global T_Data_Sobe,T_izbraniP
    
    #pathWrite="C:/Users/Hotel/Piton/PROJEKTI/UCENJE/PYQT5/Test_Designer/Test_rez.xlsx"
    #path=pathWrite
    #Pridobi podatke iz specifične tabele v excelu - iz stroj-a 

    
    # PRIDOBI PODATKE IZ SQL - podatke o sobi- iz SIFRANTSOB
    con = sqlite3.connect('C:/Users/Hotel/Piton/PROJEKTI/UCENJE/PYQT5/Test_Designer/DataBaza.db')
    T_Data_Sobe=pd.read_sql_query("SELECT * FROM SifrantSob", con)
    #print(T_Data_Sobe)
        

    #Pridobi tabelo ArhivGostov iz SQL
    T_izbraniP = pd.read_sql_query("SELECT * FROM ArhivGostov", con)
    con.close()
    
    # Pretvori datume iz sql v pandas datume
    # Iz Pandas arraya pretvori datumske stolpce v pandas datum, tako, da pandasu poveš, kakšen je format datumov v SQL (d.m.Y)
    #T_Arhiv["datumvnosa"]=pd.to_datetime(T_Arhiv["datumvnosa"],format="%d.%m.%Y")
    T_izbraniP["od"]=pd.to_datetime(T_izbraniP["od"],format="%d.%m.%Y") # Definiraš, v kakšenm formatu so datumi prišli iz SQL 
    T_izbraniP["do"]=pd.to_datetime(T_izbraniP["do"],format="%d.%m.%Y")




# Vrne list z razpoložljivimi sobami 

def proste_sobe(TipSobe,Datum_OD,Datum_DO):   
    ###############################################################
    Datum_OD= pd.Timestamp(Datum_OD)
    Datum_DO= pd.Timestamp(Datum_DO)

    PripravaPodatkov()

    L_Razp_Sobe=[]
   
    #V list daj številke vseh sob, ki imajo izbrani tip sobe
    if TipSobe == "vse":
        L_Razp_Sobe = T_Data_Sobe    
    else:
        L_Razp_Sobe=(T_Data_Sobe[T_Data_Sobe["TipSobe"]==TipSobe])
    
    L_Razp_Sobe=L_Razp_Sobe["SifraSobe"].tolist()
    
    #Iz glavne tabele izloči sobe, ki so v listu sob iskanega tipa 
    T_Filtritane_sobePRPR=T_izbraniP[T_izbraniP["stsobe"].isin(L_Razp_Sobe)]
    #print(T_Filtritane_sobePRPR.loc[:,["stsobe","od","do"]])

    #_________________________________________________________
    ### Spodnji 2 komandi sprožata opozorilo Value is trying....
    #Izloči rezervacije, ki imajo datum odhoda manjši od "Datum rezer.OD"
    T_Filtritane_sobePRPR.drop(T_Filtritane_sobePRPR[T_Filtritane_sobePRPR["do"]<=Datum_OD].index, inplace=True)
    #Izloči rezervacije, ki imajo datum prihoda večji od "Datum rezer.DO"
    T_Filtritane_sobePRPR.drop(T_Filtritane_sobePRPR[T_Filtritane_sobePRPR["od"]>=Datum_DO].index, inplace=True)
    #print(T_Filtritane_sobePRPR.loc[:,["od","do","stsobe"]])
        
    L_sobe_razpolozljive=T_Filtritane_sobePRPR["stsobe"].tolist()
    #print(L_sobe_razpolozljive)
    #print(L_Razp_Sobe)

    L_available=[]
    for i in L_Razp_Sobe:
        if i not in L_sobe_razpolozljive:
            L_available.append(i)
    
    
    #print("Razp. sobe")
    if len(L_available)==0:
        L_available.append("NI PROSTIH SOB")

    return L_available
    
# Število vrstic v ArhivGostov
def st_vrstic_gl_tabela():      #PRENOSNIK1
    return T_izbraniP.shape[0]



# List z imeni strank v tabeli

def imenaStrank():
    ListImenStrank=T_izbraniP["imestranke"].tolist()
    # Spremeni imena strank v malo pisavo, da ni problema z searchom. qt ima tudi funkcijo, ki ignorira velikost pisave
    for i in range(len(ListImenStrank)):
        ListImenStrank[i] = ListImenStrank[i].lower()

    return ListImenStrank





if __name__=="__main__":
       
    Prenosnik=proste_sobe("VSE",pd.to_datetime("2022-2-4"),pd.to_datetime("2022-2-7"))
    print(Prenosnik)








