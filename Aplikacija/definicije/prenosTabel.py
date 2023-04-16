import sqlite3
import pandas as pd
 
con = sqlite3.connect('C:/Users/Hotel/Piton/PROJEKTI/UCENJE/PYQT5/Test_Designer/DataBaza.db')
T_Arhiv = pd.read_sql_query("SELECT * FROM ArhivGostov", con)
con.close()


db=sqlite3.connect("C:/DjRezerv/MojProjekt/db.sqlite3")
    #db=sqlite3.connect("C:/DjRezerv/MojProjekt/db.sqlite3")
kurzor = db.cursor()
    
komanda = "DELETE FROM Rezervacije_vnosgostov ;"
kurzor.execute(komanda)
db.commit()
T_Arhiv.to_sql('Rezervacije_vnosgostov', db, if_exists='append', index=False)

kurzor.close()
db.close()
    