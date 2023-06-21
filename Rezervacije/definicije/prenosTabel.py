import sqlite3
import pandas as pd
 #C:\DjRezerv\MojProjekt\Rezervacije\templates\BACKUP\db.sqlite3
con = sqlite3.connect('C:/Rezervacije_QT/DataBaza.db')
T_Arhiv = pd.read_sql_query("SELECT * FROM ArhivGostov", con)
con.close()


db=sqlite3.connect("C:/DjRezerv/MojProjekt/db.sqlite3")
    #db=sqlite3.connect("C:/DjRezerv/MojProjekt/db.sqlite3")
kurzor = db.cursor()

T_Arhiv["od_dt"]=pd.to_datetime(T_Arhiv["od"], format="%d.%m.%Y")
T_Arhiv["do_dt"]=pd.to_datetime(T_Arhiv["do"], format="%d.%m.%Y")
T_Arhiv["datumVnosa_dt"]=pd.to_datetime(T_Arhiv["datumvnosa"], format="%d.%m.%Y")
T_Arhiv["status_rez"]= "rezervirano"
# T_Arhiv["cena_nocitve"]= 0
# T_Arhiv["nocitev_skupaj"]= 0
# T_Arhiv["st_noci"]= 0

T_Arhiv= T_Arhiv.drop("Noc_SK", axis=1)



komanda = "DELETE FROM Rezervacije_vnosgostov ;"
kurzor.execute(komanda)
db.commit()
T_Arhiv.to_sql('Rezervacije_vnosgostov', db, if_exists='append', index=False)

kurzor.close()
db.close()

#print(T_Arhiv)