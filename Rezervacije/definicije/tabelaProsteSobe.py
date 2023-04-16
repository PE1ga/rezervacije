import pandas as pd


#POJDI K SOSEDU po tabelo- Rez_Graf_2

def tabelaProstihSob(data, datumOd, datumDo, razpoSobe):        
    
    

    global stNocitev


    # v pandas tabeli je OBDatum na indeksu 20
    stNocitev=(datumDo-datumOd).days
    indeksOD=45 
    indeksDO=(50+stNocitev+7)  
    #print(indeksOD)

    #Naredi prazno tabelo
    T_razpSobe =pd.DataFrame(columns=data.iloc[0,:]) #Prazn5a tabela z imeni stolpcev, ki so datumi
    

    # Izloči samo sobe, ki so razpoložljive - Prenosnik 
    #Pretvori list of strings v Prenosnik v list of ints !!!!!!!!!
    for i in range(0, len(razpoSobe)): 
        if razpoSobe[i] =="NI PROSTIH SOB": 
            razpoSobe[i] = razpoSobe[i]
        else:
            razpoSobe[i] = int(razpoSobe[i])
    
    
    razpoSobe.insert(0,"xxx") #dodaj xxx, da prikaže vrstico z datumi
    razpoSobe.insert(1,"Dan") #dodaj xxx, da prikaže vrstico z imeni dni
    
    
    data = data.loc[data['S0'].isin(razpoSobe)]
    
    
    #print(data)
    
    #data=data.loc[razpoSobe,:]
    

    #Odstrani NAN
    #data=data.iloc[:,np.r_[0,indeksOD:indeksDO]]
    data = data.fillna(" ") #ostrani NaN in jih nadomesti s " "
    return data
    
