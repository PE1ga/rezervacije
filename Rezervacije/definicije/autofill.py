from django.core.files import File
import pandas as pd
import json
import os
from django.conf import settings


def PretvodiDatum(datumText):
    Mesci={"Jan":"01","Feb":"02", "Mar":"03","Apr":"04", "May":"05", "Jun":"06", "Jul":"07", 
                "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}
    Dat=datumText
    Dat_dan = Dat[0:2] ##
    Dat_mes = Dat[3:6]
    Dat_mes=Mesci[Dat_mes] ## št. mesca - uporablja dict Mesci, kjer npr. zamenja: Feb v 02
    Dat_let = Dat[9:11] ##
    
    datumBrezTexta = (str(Dat_dan) + "." + str(Dat_mes) + ".20" + str(Dat_let))
    
    return datumBrezTexta
                


def Autofill_def(tekst):
        #besedilo= open("C:/Users/Hotel/Downloads/book.txt","r",encoding='utf8')
        #vsebina = besedilo.read()
        vsebina = tekst
        
        Mesci={"Jan":"01","Feb":"02", "Mar":"03","Apr":"04", "May":"05", "Jun":"06", "Jul":"07", 
                "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}

        if "SiteMinder's DIRECT channel" in vsebina \
            or "new booking through Demand Plus" in vsebina \
            or "SiteMinder's TripAdvisor" in vsebina:
            
            # Razčleniš besedilo na vrstice
            L_vrsticeTeksta = vsebina.splitlines()   # !!!!!
            # Ustvariš list želenih fildov
            L_iscem = ["Grand Total: €","Check In Date:", 
                    "Check Out Date:","Guest Name:", "Guest ETA:", "Guest Comments:"] #   "[SiteMinder] Booking for ", "Guest ETA:", "Guest Comments:"] #dec 22 siteminder daje manj osebnih podatkov, zato sem spremenil ta list-- "Guest Name:", "Guest Email:", "Guest Comments:"]
            ListFildov = []
            for iscem in L_iscem:
                IskanaVrsticaVListu = next((s for s in L_vrsticeTeksta if iscem in s), None) # Dobiš:     Check In Date: 17 Jul 2022       !!!!!!
                Skrap = IskanaVrsticaVListu.replace(iscem,"")    # Dobiš rezultat z whitesplacem:   17 Jul 2022   
                
                Skrap=Skrap.strip() # Odstrani desni whitespace, ki nastane pri sitemind.
                if L_iscem.index(iscem) == 3:
                    skrap2 = Skrap.split("(")[0]
                     
                    ListFildov.append(skrap2)
                else:
                    ListFildov.append(Skrap)
            
            #Na koncu dodaj še ime agencije
            ListFildov.append("Siteminder")
            
            # Popravi ceno na poziciji 0 - odstrani vejico
            CenaSitem = ListFildov[0].replace(",","")
            ListFildov[0]=CenaSitem
            
            # Multiroom - če je multiroom, potem ceno vnesi ročno. V listu na poziciji 0 dodaj tekst "MR" 
            if "Room 1:" in vsebina:
                ListFildov[0]= ""



            # Ugotovi, ali je rz. nonrefundable. Če da, potem v polje RNA vnesi NONREFOK, saj sedaj Siteminder avtomatsko
            # zaračuna 100% avans pri nonref rezervaciji-
            if "Room 1:" in vsebina:
                AliNonRef = vsebina.split("Room 1:")[1]
            else:
                AliNonRef = vsebina.split("Room:")[1]  # najprej izoliraj sobo, da bo rezultat bolj natančen- Family Room with Balcony and Mountain View / Non-Refundable
            
            AliNonRef = AliNonRef.splitlines()[0]
            rna=""
            if "Non-Refundable" in AliNonRef:
                rna = "NONREFOK"
            
           
            
            # VRNI V view.py
            cena = ListFildov[0] 
            ime = ListFildov[3].lower().title()
            agencija = "Siteminder"
            stoseb = 2
            od = PretvodiDatum(ListFildov[1])
            do = PretvodiDatum(ListFildov[2])
            rna=rna
            rmail = ListFildov[4]
            zahteve = ListFildov[5]
            #print(DatumOD, DatumDO)

            #return cena, ime, agencija, StOseb, DatumOD, DatumDO, RNA




        elif "Booking.com" in vsebina or "Expedia" in vsebina:
            L_iscem = ["Total Price:","Check In Date:", "Check Out Date:",
                    "Booker Name:", "Booker Email:", "Remarks:" ]
            ListFildov = []
            for iscem in L_iscem:
                # try exc zato, ker pri Expedia rezervaciji HotelCollect ni opcije Booker Email: , zato pride do napake.
                try:
                    Skrap= vsebina.split(iscem)
                    
                    Skrap = Skrap[1]
                    Skrap=Skrap.splitlines()
                    Skrap = Skrap[2]
                    ListFildov.append(Skrap)
                except:
                    ListFildov.append("Ni podatka")

            #Na koncu dodaj še ime agencije
            if "Booking.com" in vsebina:
                ListFildov.append("Booking.com") 
            elif "Expedia" in vsebina:
                ListFildov.append("Expedia") 

            
            # Odstrani EUR iz cene
            Cena=ListFildov[0].replace(" EUR","")
            ListFildov[0] = Cena
            # Odstrani , iz imena stranke  
            Stranka = ListFildov[3].replace(",","")
            ListFildov[3] = Stranka      

            
            """# Multiroom - če gre za več sob, dodaj v listu na pozicijo 0 (cena) tekst "MR"
            # Razčleniš besedilo na vrstice
            List_vrstic = vsebina.splitlines() 
            df = pd.DataFrame({'Text': List_vrstic})
            st_stavkov= (df[df["Text"]=="Total Price:"].count())  # pri rezervaciji samo 1 sobe se "Total Price:" pojavi 2x, pri MR pa >2
            if st_stavkov.item() > 2:  
                self.Multiroom = True  
                ListFildov[0] = ""   """

            rna=""
            # Ugotovi, ali imaš Virtual credit card- če da, potem vnesi ExpColl v obrazec
            # Dodatne zahteve so v listu pod index = 5
            if ListFildov[5].find("virtual credit card") != -1 or ListFildov[5].find("Expedia Collect Booking") != -1: #!!!!! If find() doesn't find a match, it returns -1, otherwise it returns the left-most index of the substring in the larger string.
                rna=("ExpColl")
                #self.RNA.setEnabled(False)
           
            # Ali gre pri expediji za Hotel Collect booking
            if ListFildov[5].find("Hotel Collect Booking") != -1:
                rna=("refOK")
                #self.RNA.setEnabled(False)


            # Ali ima rezervacija Non-refundable-  če da, potem je RNA fild = NONref
            AliNonRefBookingCom = vsebina.split("ROOM - ")[1]  # najprej izoliraj sobo, da bo rezultat bolj natančen::: Economy Double Room with Forest View - Non-refundable - Breakfast included
            AliNonRefBookingCom = AliNonRefBookingCom.splitlines()[0]
            #print(AliNonRefBookingCom)
            
            if "Non-refundable" in AliNonRefBookingCom:
                rna="NONref"
                #self.RNA.setEnabled(False)

            # VRNI V view.py
            cena = ListFildov[0] 
            ime = ListFildov[3].lower().title()
            agencija = "Booking.com"
            stoseb = ""
            od = PretvodiDatum(ListFildov[1])
            do = PretvodiDatum(ListFildov[2])
            rmail = ListFildov[4]
            zahteve = ListFildov[5]
            rna=rna
            #return cena, ime, agencija, StOseb, DatumOD, DatumDO, RNA


    # HOTELBEDS _____________________________________


        elif "Hotelbeds" in vsebina:
            L_iscem = ["Total Booking Cost Inc. Tax:","Check In Date:", "Check Out Date:",
                    "Room Guests:", "Booker Email::", "Remarks:" ]
            ListFildov = []
            for iscem in L_iscem:
                # try exc zato, ker pri HotelBeds rezervaciji HotelCollect ni opcije Booker Email: , zato pride do napake.
                try:
                    Skrap= vsebina.split(iscem)
                    
                    Skrap = Skrap[1]
                    Skrap=Skrap.splitlines()
                    Skrap = Skrap[2]
                    ListFildov.append(Skrap)
                except:
                    ListFildov.append("Ni podatka")

            #Na koncu dodaj še ime agencije
            
            ListFildov.append("HotelBEDS") 
            
            
            # Odstrani EUR iz cene
            Cena=ListFildov[0].replace(" EUR","")
            ListFildov[0] = Cena

        elif "Agoda Booking ID" in vsebina:
            L_iscem = ["Net rate (incl. taxes & fees)\n\nEUR ","Check In Date:", "Check Out Date:",
                    "Room Guests:", "Booker Email::", "Remarks:" ]
            ListFildov = []
            for iscem in L_iscem:
                # try exc zato, ker pri HotelBeds rezervaciji HotelCollect ni opcije Booker Email: , zato pride do napake.
                try:
                    Skrap= vsebina.split(iscem)
                    print(Skrap)
                    
                    Skrap = Skrap[1]
                    Skrap=Skrap.splitlines()
                    Skrap = Skrap[2]
                    ListFildov.append(Skrap)
                except:
                    ListFildov.append("Ni podatka")

            #Na koncu dodaj še ime agencije
            
            ListFildov.append("Agoda") 
            print(ListFildov)
            
            
            # Odstrani EUR iz cene
            Cena=ListFildov[0].replace(" EUR","")
            ListFildov[0] = Cena







        else:
            print("To ni Siteminder, Expedia ali Booking.com")
            return



        # SKUPNA OBDELAVA ZA VSE AGENCIJE
       # PRENOS V JSON

        JS_file = os.path.join(settings.BASE_DIR, 'Rezervacije//static//json//jsonFILE_IzborSob.json')
        # izprazni json
        with open(JS_file, "w", encoding="utf-8") as f:
            json.dump({0:0}, f, ensure_ascii=False, indent=4)
        
        #with open(JS_file, "r", encoding="utf-8") as f:
          #  jsonData = json.load(f)
        jsonData= {}
        jsonData["avtovnos"]= True
        jsonData["cena"] = cena
        jsonData["ime"] = ime
        jsonData["agencija"] = agencija
        jsonData["stoseb"] = stoseb
        jsonData["od"] = od
        jsonData["do"] = do
        jsonData["rna"] = rna
        jsonData["email"] = rmail
        jsonData["zahteve"] = zahteve


        print(jsonData)
           
        with open(JS_file, "w", encoding="utf-8") as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)


        #return cena, ime, agencija, StOseb, DatumOD, DatumDO, RNA, Email, Zahteve
        return od, do, ime










            # JSON 
            # 0: Razpoložljive sobe, 
            #  1: Od
            #  2: Do
            #  3: Tip 
            #  4: Ime
            #  5: Št oseb
            #  6: Št Sobe
            #  7: Cena
            #  8: Agencija
            #  9: Država
            #  10: RNA
            #  11: Zahteve
            #  12: email    
            
        
            
#Zaženi
if __name__==("__main__"):
    Autofill_def()