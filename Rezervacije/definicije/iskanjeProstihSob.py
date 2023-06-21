#PROGRAM ZA ISKANJE PROSTIH SOB NEKEGA TIPA V DOLOČENEM TERMINU
import pandas as pd
import warnings # to je za Pandas erorrrje
warnings.filterwarnings("ignore")
#import sqlite3


"""T_Data_Sobe = ""
T_izbraniP = ""

def PripravaPodatkov():
    
    global T_Data_Sobe,T_izbraniP
    # PRIDOBI PODATKE IZ SQL - podatke o sobi- iz SIFRANTSOB
    con = sqlite3.connect('C:/DjRezerv/MojProjekt/db.sqlite3')
    T_izbraniP = pd.read_sql_query("SELECT * FROM Rezervacije_vnosgostov", con)
    
    
    #con = sqlite3.connect('C:/Rezervacije_QT/DataBaza.db')
    T_Data_Sobe=pd.read_sql_query("SELECT * FROM Rezervacije_sifrantsob", con)
   
    
    #print(T_Data_Sobe)
        

    
    con.close()
    
    # Pretvori datume iz sql v pandas datume
    # Iz Pandas arraya pretvori datumske stolpce v pandas datum, tako, da pandasu poveš, kakšen je format datumov v SQL (d.m.Y)
    #T_Arhiv["datumvnosa"]=pd.to_datetime(T_Arhiv["datumvnosa"],format="%d.%m.%Y")
    T_izbraniP["od"]=pd.to_datetime(T_izbraniP["od"],format="%d.%m.%Y") # Definiraš, v kakšenm formatu so datumi prišli iz SQL 
    T_izbraniP["do"]=pd.to_datetime(T_izbraniP["do"],format="%d.%m.%Y")




# Vrne list z razpoložljivimi sobami 
"""
def proste_sobe(T_izbraniP, T_Data_Sobe, TipSobe, Datum_OD, Datum_DO):   
    ###############################################################
    #global T_Data_Sobe,T_izbraniP

    T_izbraniP["od"]=pd.to_datetime(T_izbraniP["od"],format="%d.%m.%Y") # Definiraš, v kakšenm formatu so datumi prišli iz SQL 
    T_izbraniP["do"]=pd.to_datetime(T_izbraniP["do"],format="%d.%m.%Y")
    Datum_OD= pd.to_datetime(Datum_OD, format="%d.%m.%Y")     #  pd.Timestamp(Datum_OD)
    Datum_DO= pd.to_datetime(Datum_DO, format="%d.%m.%Y")     # pd.Timestamp(Datum_DO)
    

    #PripravaPodatkov()

    L_Razp_Sobe=[]
   
    #V list daj številke vseh sob, ki imajo izbrani tip sobe
    if TipSobe == "vse":
        L_Razp_Sobe = T_Data_Sobe    
    else:
        L_Razp_Sobe=(T_Data_Sobe[T_Data_Sobe["TipSobe"]==TipSobe])
    
    L_Razp_Sobe=L_Razp_Sobe["SifraSobe"].tolist()
    L_Razp_Sobe.append(99)
    
    #Iz glavne tabele izloči sobe, ki so v listu sob iskanega tipa 
    T_Filtritane_sobePRPR= T_izbraniP[T_izbraniP["stsobe"].isin(L_Razp_Sobe)]
    #print(T_Filtritane_sobePRPR.loc[:,["stsobe","od","do"]])

    #_________________________________________________________
    ### Spodnji 2 komandi sprožata opozorilo Value is trying....
    #Izloči rezervacije, ki imajo datum odhoda manjši od "Datum rezer.OD"
    T_Filtritane_sobePRPR.drop(T_Filtritane_sobePRPR[T_Filtritane_sobePRPR["do"]<=Datum_OD].index, inplace=True)
    #Izloči rezervacije, ki imajo datum prihoda večji od "Datum rezer.DO"
    T_Filtritane_sobePRPR.drop(T_Filtritane_sobePRPR[T_Filtritane_sobePRPR["od"]>=Datum_DO].index, inplace=True)
    #print(T_Filtritane_sobePRPR.loc[:,["od","do","stsobe"]])
    #print(T_Filtritane_sobePRPR.loc[:,["stsobe","od","do"]])
    L_sobe_razpolozljive=T_Filtritane_sobePRPR["stsobe"].tolist()
    

    L_available=[]
    for i in L_Razp_Sobe:
        if i not in L_sobe_razpolozljive:
            L_available.append(i)
    #print(L_available)
    
    #print("Razp. sobe")
    if len(L_available)==0:
        L_available.append("NI PROSTIH SOB")

    return L_available
    


def prosteSobeZaPonudbo(T_izbraniP, T_Data_Sobe, odDatum, doDatum):
    listSob = ["x","y","c","s","g","q","d","f"]
    dictProstihSob = {}
    for tipSobe in listSob:
        L_prosteSobe= proste_sobe(T_izbraniP, T_Data_Sobe, tipSobe, odDatum, doDatum)
        if L_prosteSobe[0] == "NI PROSTIH SOB":
            dictProstihSob[tipSobe]=0
        else: 
            dictProstihSob[tipSobe]=len(L_prosteSobe)
    
    return dictProstihSob



"""

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
"""




if __name__=="__main__":
    pass
    """Prenosnik=proste_sobe("c",pd.to_datetime("2023-2-14"),pd.to_datetime("2023-2-15"))
    print(Prenosnik)"""








