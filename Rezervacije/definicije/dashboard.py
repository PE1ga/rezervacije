import pandas as pd
from datetime import datetime

class Dashboard:
    def __init__(self, df_data_rezervirano, df_data_odpovedano, leto) -> None:
        self.df_data_rezervirano = df_data_rezervirano
        self.df_data_odpovedano= df_data_odpovedano
        self.leto = str(leto)
        self.danes = pd.to_datetime("today")
        

        # REZERVIRANO
        self.t_izbrani_p_rezerv = self.df_data_rezervirano    
        self.t_izbrani_p_rezerv["datumvnosa"]=pd.to_datetime(self.t_izbrani_p_rezerv["datumvnosa"],format="%d.%m.%Y").dt.normalize()
        self.t_izbrani_p_rezerv["od"]=pd.to_datetime(self.t_izbrani_p_rezerv["od"],format="%d.%m.%Y").dt.normalize()
        self.t_izbrani_p_rezerv["do"]=pd.to_datetime(self.t_izbrani_p_rezerv["do"],format="%d.%m.%Y").dt.normalize()

        # oO > 1.1.2021
        self.t_podatki_leto=self.t_izbrani_p_rezerv[self.t_izbrani_p_rezerv["do"]>=pd.to_datetime("1.1." + self.leto,format="%d.%m.%Y")] 
        # DO < 31.12.2021
        self.t_podatki_leto=self.t_podatki_leto[self.t_podatki_leto["do"]<=pd.to_datetime("31.12." + self.leto,format="%d.%m.%Y")] 
        self.t_podatki_leto["StNocitevSK"]=(self.t_podatki_leto["SO"]*(self.t_podatki_leto["do"]-self.t_podatki_leto["od"])).dt.days
        
        # ODPOVEDANO
        self.t_izbrani_p_odpoved = self.df_data_odpovedano
        self.t_izbrani_p_odpoved["datumvnosa"]= pd.to_datetime(self.t_izbrani_p_odpoved["datumvnosa"], format="%d.%m.%Y").dt.normalize()
        self.t_izbrani_p_odpoved["od"]= pd.to_datetime(self.t_izbrani_p_odpoved["od"], format="%d.%m.%Y").dt.normalize()
        self.t_izbrani_p_odpoved["do"]= pd.to_datetime(self.t_izbrani_p_odpoved["do"], format="%d.%m.%Y").dt.normalize()






    def nocitve_in_eur_po_mescih(self):
        # PRIHODEK PO MESCIH 2021
        #T_PodDRZAVAH=(T_PodDrzavah.groupby(['DR',"ImeMeseca"],as_index=False).agg({'SO': 'sum', 'StNocitevSK': 'sum','CENA': 'sum'}))
        t_rezultati_po_mescih = self.t_podatki_leto.groupby([self.t_podatki_leto['do'].dt.year.rename('y'), 
                                                    self.t_podatki_leto['do'].dt.month.rename('m')],as_index=True).agg({'CENA':'sum', 'StNocitevSK': 'sum'})      
        t_rezultati_po_mescih= t_rezultati_po_mescih.reset_index().rename(columns={"CENA":"cena", "StNocitevSK":"nocitev"})
        
        t_rezultati_po_mescih = t_rezultati_po_mescih.astype(int) # zato, da ni decimalk v rezultatu
        
        return t_rezultati_po_mescih


        # ŠTEVILO NOČITEV PO MESCIH 2021
        #t_st_nocitev=(t_podatki_leto.groupby([t_podatki_leto['do'].dt.year.rename('y'), t_podatki_leto['do'].dt.month.rename('m')]).sum()["StNocitevSK"]).to_frame(name="Št Nočitev").reset_index()
        #t_st_nocitev = t_st_nocitev.astype(int)



    def lista_gostov_danes(self):
        stayover = self.t_izbrani_p_rezerv[(self.t_izbrani_p_rezerv["od"]<= self.danes) & (self.t_izbrani_p_rezerv["do"]> self.danes)]
        prihodi = self.t_izbrani_p_rezerv[self.t_izbrani_p_rezerv["od_dt"]== self.danes]
        lista_gostov = pd.concat([stayover,prihodi], axis=0).sort_values("stsobe")
        
        return lista_gostov
    
    def zadnje_rezervacije_danes(self):
        zadnje_rezervacije = self.t_izbrani_p_rezerv.head(13).sort_values(by= "datumvnosa", ascending= False )
        return zadnje_rezervacije
    
    def zadnje_odpovedi_danes(self):
        zadnje_odpovedi = self.t_izbrani_p_odpoved[self.t_izbrani_p_odpoved["do"]>= pd.to_datetime(("1.1." + self.leto), format="%d.%m.%Y")].tail(5)
        return zadnje_odpovedi
    
    def profit_po_agencijah(self):
        profit_po_agenciji = self.t_podatki_leto.groupby("agencija")["CENA"].sum().to_frame(name="Cena").reset_index()
        profit_po_agenciji["Cena"] = profit_po_agenciji["Cena"].astype(float)
        profit_po_agenciji["Cena"]= profit_po_agenciji["Cena"].round(2) 
        profit_po_agenciji = profit_po_agenciji.sort_values(by="Cena", ascending= False)
        
        print(profit_po_agenciji)
        return profit_po_agenciji


        #T_profitAG2021=T_Podatki2021.groupby("agencija").sum()["CENA"].to_frame(name="Cena").reset_index() #!!!!!!
        #T_profitAG2021["Cena"]=T_profitAG2021["Cena"].round(2)
        #T_profitAG2021 = T_profitAG2021.sort_values(by="Cena", ascending=False)

if __name__=="__main__":
    Dashboard.rezultati_po_mescih("data", "2022")

