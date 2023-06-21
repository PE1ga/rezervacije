

def info_tekst_def(ime, agencija, drzava, stoseb, tip, multiroom):
    if agencija == "Booking.com" or agencija == "Siteminder": #, or Agencija == "Expedia"
        if multiroom == True:
            if drzava !="SI":
                sporocilo = (f"""
                --This message was sent automatically - Please don't reply.--
                <br><br>
                Dear {ime}!
                <br><br>
                Thank you for your reservation.
                <br><br>
                Some important information:
                <br><br>
                CHILDREN POLICY:
                <br>- If there are any children on your reservation, please note, that we only accept children older than 5 years of age.
                <br><br>
                MAXIMUM OCCUPANCY:
                <br>- Double rooms have a maximum occupancy of 2 people.
                <br>- Quadruple rooms rooms have a maximum occupancy of 4 people.
                <br>
                <br>If there will be more guests on check-in than allowed, any extra guests will not be accepted.
               <br> <br> 
                CHECK IN:
                <br>- After 14:00.
                <br>- On check in we will need the IDs or passports of all people.
                <br><br>
                DINNING OPTIONS:
                <br>- We are B&B Hotel and we don't offer dinners. There are restaurants within walking distance.
                
                <br><br>
                Kind regards,
                <br><br>
                Hotel Gašperin Bohinj
                
                """)
                
                return sporocilo
        
        
            elif drzava == "SI": # ZA SLOVENIJO - multiroom rezervacija
                    sporocilo = (f"""
                    --To sporočilo je bilo poslano avtomatsko.--
                    <br><br>
                    Spoštovani {ime}!
                    <br><br>
                    Zahvaljujemo se za vašo rezervacijo.
                    <br><br>
                    Pošiljamo naslednje informacije:
                    <br><br>
                    PRAVILA GLEDE OTROK:
                    <br>- Če so v rezervaciji tudi otroci, vas obveščamo, da sprejemamo otroke starejše od 5 let.
                    <br><br>
                    NAJVEČJE DOVOLJENO ŠTEVILO OSEB V SOBAH:
                    <br>- V dvoposteljnih sobah sta vključno z otroci dovoljeni največ 2 osebi.
                    <br>- V štiriposteljnih sobah so vključno z otroci dovoljene največ 4 osebe.
                    <br><br>
                    <br>Če bo ob prijavi število oseb višje od dovoljenega, dodatne osebe ne bodo sprejete.
                    <br><br>
                    PRIJAVA:
                    <br>- Po 14:00.
                    <br>- Na recepciji bomo za prijavo potrebovali osebne dokumente od vseh oseb.
                    <br><br>
                    MOŽNOST KOSILA / VEČERJE:
                    <br>Naš hotel je kategoriziran kot Garni hotel, kar pomeni, da nudimo nočitev z zajtrkom. 
                    <br>Kosila in večerje ne nudimo. V bližini našega hotela je mnogo restavracij.
                    <br><br>
                    Lep pozdrav,
                    <br><br>
                    Hotel Gašperin Bohinj

                        """)
                    
                    return sporocilo
            
        # Rezervacija ni Multiroom, ampak samo 1 soba: ######################## INDIVIDUALNA!!!
            
        else:
            # Priprava tekstov
            #  SLO teksti - specifika- sklanjanje       
            if tip =="c" or tip == "f" or tip =="x"or tip =="g" or tip =="s" or tip =="y":
                maxStevOsebvSobi = "2 people"
                maxStevOsebvSobiSLO = "sta dovoljeni največ 2 osebi"
            elif tip =="q" or tip == "d":
                maxStevOsebvSobi = "4 people"
                maxStevOsebvSobiSLO = "so dovoljene največ 4 osebe"
            # elif tipSobe =="y":
            #     maxStevOsebvSobi = "1 person"
            #     maxStevOsebvSobiSLO = "je dovoljena največ 1 oseba"

            
            
            # Če je rezvirano manj oseb, kot je max kapaciteta sobe

            if tip =="c" or tip == "f" or tip =="x"or tip =="g" or tip =="s" or tip =="y":
                if int(stoseb) == 2:
                    if drzava != "SI": 
                        MaxZadedenostObvestilo = """
                        MAXIMUM OCCUPANCY:
                        <br>- The room that you booked has a maximum occupancy of """ + maxStevOsebvSobi + """. 
                        <br>If there will be more guests on check-in than allowed, any extra guests will not be accepted.
                        """
                    elif drzava == "SI":
                        MaxZadedenostObvestilo = """
                        NAJVIŠJE DOVOLJENO ŠTEVILO OSEB V SOBI:
                        <br>- V sobi, ki ste jo rezervirali, """+ maxStevOsebvSobiSLO + """.
                        <br>Če bo ob prijavi število oseb višje od dovoljenega, dodatne osebe ne bodo sprejete.
                        """

                # Rezervacija - samo 1 oseba v dvoposteljni:
                else: 
                    if drzava != "SI": 
                        MaxZadedenostObvestilo = """OCCUPANCY:  
                        <br>- You reserved a double room for """ + stoseb + """ person. If there will be more than """ + stoseb + """ person, 
                        <br>the price of the reservation will be higher. The room that you booked has a maximum occupancy of """ + maxStevOsebvSobi + """.""" 
                    elif drzava == "SI":
                        MaxZadedenostObvestilo = """REZERVACIJA:
                        <br>- Rezervirali ste dvoposteljno sobo za 1 osebo. Če bo ob prijavi več oseb kot 1, bo cena rezervacije višja. 
                        <br>Najvišje dovoljeno število oseb v tej sobi je """+ maxStevOsebvSobi + """.
                        """
            
            elif tip =="q" or tip == "d":
                if int(stoseb) == 4:
                    if drzava != "SI": 
                        MaxZadedenostObvestilo = """
                        MAXIMUM OCCUPANCY:
                        <br>- The room that you booked has a maximum occupancy of """ + maxStevOsebvSobi + """.  
                        <br>If there will be more guests on check-in than allowed, any extra guests will not be accepted.
                        """
                    elif drzava == "SI":
                        MaxZadedenostObvestilo = """
                        NAJVIŠJE DOVOLJENO ŠTEVILO OSEB V SOBI:
                        <br>- V sobi, ki ste jo rezervirali, """+ maxStevOsebvSobiSLO + """.
                        <br>Če bo ob prijavi število oseb višje od dovoljenega, dodatne osebe ne bodo sprejete.
                        """




                # Rezervacija - samo manj kot 4 osebe v štiriposteljni:
                else: 
                    if drzava != "SI":
                        MaxZadedenostObvestilo = """OCCUPANCY:
                        <br>- You reserved a quadruple room for """ + stoseb + """ person. If there will be more than """ + stoseb + """ persons, 
                        the price of the reservation will be higher. The room that you booked has a maximum occupancy of """ + maxStevOsebvSobi + """.""" 
                    elif drzava == "SI":
                        MaxZadedenostObvestilo = """REZERVACIJA:
                        <br>- Rezervirali ste štiriposteljno sobo za št. oseb: """ + stoseb + """. Če bo ob prijavi več oseb kot """ + stoseb + """, bo cena rezervacije višja. 
                        V tej sobi """+ maxStevOsebvSobiSLO + """.
                        """

          
            
            # ____________
            # Dodatni opis sobe - npr. Ground floor no elevator, ...
            DodatniOpisSob = " "
            if tip == "g":
                if drzava != "SI":
                    DodatniOpisSob ="""                                    
                    ROOM AND ACCESS:
                    <br>- Comfortable room located on the car park level. Please note that to reach the room, you will need to use
                    a short staircase of 15 steps (no elevator). Your room has a desk and a private patio for you to relax and enjoy the fresh air. 
                    <br>Room is equipped with air conditioning and a bathroom featuring a shower and WC.
                    
                    """
                
                elif drzava == "SI":
                    DodatniOpisSob ="""
                    SOBA IN DOSTOP:
                    <br>- Kot je navedeno v opisu sobe na spletni strani, se soba nahaje v pritličju na istem nivoju kot parkirišče.
                    <br>Do sobe ni dostopa z dvigalom, ampak do tja vodi 1 stopnišče.
                    """
            
            if tip == "x":
                if drzava !="SI":
                    DodatniOpisSob ="""                                    
                    ROOM:
                    <br>- Our cozy Economy double room is the perfect choice for a comfortable and affordable stay. 
                    <br>With a size of 12m2, this room is compact but offers everything you need for a restful stay, 
                    including a comfortable double bed, a desk, and a private toilet with a shower and WC. 
                    <br>Please note that this room does not have a balcony. 
                    <br>This room has view of the forest.
                    """
                elif drzava =="SI": 
                    DodatniOpisSob = """
                    SOBA:
                    <br>- Rezervirali ste Dvoposteljno sobo Economy. Soba s površino 12m2 je kompaktna, 
                    vendar kljub temu nudi vse za prijetno in ugodno bivanje v našem hotelu. 
                    <br>Ima klimo, udobno dvojno posteljo, hladilnik, kopalnico s tušem in wc. Soba nima balkona. 
                    <br>Nahaja se v zgornjem nadstropju in ima razgled na gozd.
                    """
            
            if tip == "y":
                if drzava !="SI":
                    DodatniOpisSob ="""                                    
                    ROOM:
                    <br>- Our cozy Economy double attic room is the perfect choice for a comfortable and affordable stay. 
                    <br>With a size of 12m2, this room offers everything you need for a restful stay, 
                    including a comfortable double bed, a desk, and a private toilet with a shower and WC. 
                    <br>Please note that this room does not have a balcony. 
                    <br>This room has view of the forest.
                    """
                elif drzava =="SI": 
                    DodatniOpisSob = """
                    SOBA:
                    <br>- Rezervirali ste Dvoposteljno sobo Economy. Soba s površino 12m2 nudi vse za prijetno in 
                    ugodno bivanje v našem hotelu. Ima klimo, udobno dvojno posteljo, hladilnik, kopalnico s 
                    tušem in wc. Soba nima balkona. Nahaja se v zgornjem nadstropju in ima razgled na gozd.
                    """
            
            
            #_____________ konec dodatnih opisov sob
            
            # KONČNI TEKSTI
            # BACKUP 
                # MAXIMUM OCCUPANCY:
                # - The room that you booked has a maximum occupancy of {maxStevOsebvSobi}. 
                # If there will be more guests on check-in than allowed, any extra guests will not be accepted.
                    
                # GB:
            if drzava !="SI":
                sporocilo = (f"""
                --This message was sent automatically - Please don't reply.--
                <br><br>
                Dear {ime}!
                <br><br>
                Thank you for your reservation.
                <br>
                Some important information:
                <br><br>
                CHILDREN POLICY:<br>
                - If there are any children on your reservation, please note, that we only accept children older than 5 years of age.
                <br><br>
                {MaxZadedenostObvestilo}
                <br><br>
                CHECK IN:
                <br>- After 14:00.
                <br>- On check in we will need the IDs or passports of all people.
                <br><br>
                {DodatniOpisSob}
                <br><br>
                DINNING OPTIONS:
                <br>- We are B&B Hotel and we don't offer dinners. There are restaurants within walking distance.
                <br><br>
                Kind regards,
                <br><br>
                <br>Hotel Gašperin Bohinj
                
                """)
                
                return sporocilo
            
            
            elif drzava == "SI": # ZA SLOVENIJO
                sporocilo = (f"""
            --To sporočilo je bilo poslano avtomatsko.--
            <br><br>
            Spoštovani {ime}!
            <br><br>
            Zahvaljujemo se za vašo rezervacijo.
            <br><br>
            Nekaj informacij:
            <br><br>
            MINIMALNA STAROST OTROK:
            <br>- Če so v rezervaciji tudi otroci, vas obveščamo, da sprejemamo otroke starejše od 5 let.
            <br><br>
            {MaxZadedenostObvestilo}
            <br><br>
            OSEBNI DOKUMENTI:
            <br>- Na recepciji bomo za prijavo potrebovali osebne dokumente od vseh oseb.
            <br>{DodatniOpisSob}
            <br>MOŽNOST KOSILA / VEČERJE:
            <br>Naš hotel je kategoriziran kot Garni hotel, kar pomeni, da nudimo nočitev z zajtrkom. 
            <br>Kosila in večerje ne nudimo. V bližini našega hotela je mnogo restavracij.
            <br><br>
            Lep pozdrav,
            <br><br>
            Hotel Gašperin Bohinj
            <br>
                """)
                
                return sporocilo