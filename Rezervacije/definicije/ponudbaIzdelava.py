from string import Template
import pandas as pd
from datetime import datetime


def ponudba_izdelava_Html(dictPonudba):
    jezik = dictPonudba["jezik"]
    rna = dictPonudba["rna"]
    if jezik == "SLO":
        jezik = 0
    elif jezik == "GB":
        jezik = 1
    odDat = dictPonudba["od"]
    doDat = dictPonudba["do"]
    stNoci= (pd.to_datetime(doDat, format="%d.%m.%Y") - pd.to_datetime(odDat, format="%d.%m.%Y")).days
    ImeStranke = dictPonudba["ime"]
    strosekOdpovedi ="100"
    AvansEUR = dictPonudba["avans"]
    odpovedniRok = dictPonudba["odpoved"]
    datumOdpovedniRok = (pd.to_datetime(odDat, format="%d.%m.%Y")- pd.Timedelta(days=int(odpovedniRok))).strftime('%d.%m.%Y')
    multiroom = len(dictPonudba["tipSobe"])
    vrstaInAli = dictPonudba["vrstaInAli"]
    zahteve = dictPonudba["zahteve"]
    if multiroom > 1 :
        multiroom = True
    
    sedaj = datetime.now().hour
    
    if sedaj < 12:
        pozdrav =["Dobro jutro ", "Good morning "]
    elif sedaj < 18:
        pozdrav =["Dober dan", "Good afternoon "]
    else:
        pozdrav =["Dober večer", "Good evening "]
    
    ### TEKSTI ###
    
        ### SLO ###
    header={
        "pozdrav": [f"<h3><b>{pozdrav[jezik]} {ImeStranke}!</b></h3><br>Hvala za povpraševanje.",
                    f"<h3><b>{pozdrav[jezik]} {ImeStranke}!</b></h3><br>Thank you for your inquiry."],
        
        "uvod": [f"<br>Za obdobje od {odDat} do {doDat} (število nočitev {stNoci}), lahko ponudimo:",
                f"<br>For the period from {odDat} to {doDat} (number of nights {stNoci}), we can offer you:"],
        
        "cena": ["""<br><br><b>CENA:</b><br>Storitev: nočitev z zajtrkom<br>Število oseb: $stOsebSK 
                    <br>Število nočitev: $stNoci <br>Cena nastanitve: $CenaBrezTTax EUR
                    <br>Turistična taksa: $TtaxSkupaj EUR<br><b>NASTANITEV SKUPAJ: $koncnaCena EUR</b>""",
                """<br><br><b>PRICE:</b><br>Service: Bed & Breakfast<br>Number of persons: $stOsebSK 
                    <br>Number of nights: $stNoci <br>Price for accommodation: $CenaBrezTTax EUR<br>
                    Tourist tax: $TtaxSkupaj EUR<br><b>ACCOMMODATION TOTAL: $koncnaCena EUR</b>  """],
    }

    sobeOpisi={
        "x": ["""<br><br><b>Economy dvoposteljna soba 12m2.</b> 
            <br>Oprema sobe: KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI.
            <br><a href=https://www.gasperin-bohinj.com/nastanitev-gasperin-hotel-bohinj/economy-dvoposteljna-soba>
            Za več informacij KLIKNITE TU.</a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br><b>Economy double room 12m2.</b> 
            <br>Room amenities: AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI. 
            <br><a href= https://www.bohinj-hotel-gasperin.com/rooms-bohinj/economy-double-room-with-forest-view.html>
            CLICK HERE for detailed description</a> <br> Free parking at the hotel."""],
        
        "y": ["""<br><br><b>Economy dvoposteljna podstrešna soba 12m2.</b> 
            <br>Oprema sobe: KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI.  
            <br><a href=https://www.bohinj-hotel-gasperin.com/rooms-bohinj/economy-double-attic-room-with-forest-view.html>
            Za več informacij KLIKNITE TU. </a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br> <b>Economy Double Attic Room 12m2.</b> 
            <br>Room amenities: AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI.  
            <br><a href=https://www.bohinj-hotel-gasperin.com/rooms-bohinj/economy-double-attic-room-with-forest-view.html>
            CLICK HERE for detailed description. </a><br> Free parking at the hotel."""],
        
        "g": ["""<br><br><b>Dvoposteljna soba s pogledom na gore- pritličje</b> 
            <br>Oprema sobe: KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI, TERASA. 
            <br><a href= https://www.gasperin-bohinj.com/nastanitev-gasperin-hotel-bohinj/dvoposteljna-soba-s-pogledom-na-gore-pritlicje/>  
            Za več informacij KLIKNITE TU</a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br> <b>Double Room with Mountain View and Ground Floor.</b> 
            <br>Room amenities: PATIO, AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI. 
            <br><a href=https://www.bohinj-hotel-gasperin.com/rooms-bohinj/double-room-with-mountain-view-ground-floor.html>  
            CLICK HERE for detailed description</a><br> Free parking at the hotel."""],

        "f": ["""<br><br><b>Dvoposteljna soba z balkonom in pogledom na gozd.</b> 
            <br>Oprema sobe: BALKON, KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI. 
            <br><a href= https://www.gasperin-bohinj.com/nastanitev-gasperin-hotel-bohinj/dvoposteljna-soba-z-balkonom-in-pogledom-na-gozd > 
            Za več informacij KLIKNITE TU</a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br><b>Double Room with Balcony and Forest view.</b> 
            <br>Room amenities: BALCONY, AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI). 
            <br><a href= https://www.bohinj-hotel-gasperin.com/rooms-bohinj/double-room-with-balcony-and-forest-view.html >  
            CLICK HERE for detailed description</a><br> Free parking at the hotel."""],
        
        "c": ["""<br><br><b>Dvoposteljna soba z balkonom in pogledom na gore.</b> 
            <br>Oprema sobe: BALKON, KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI.
            <br><a href=https://www.gasperin-bohinj.com/nastanitev-gasperin-hotel-bohinj/dvoposteljna-soba-z-balkonom-in-pogledom-na-gore > 
            Za več informacij KLIKNITE TU</a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br><b>Double Room with Balcony and Mountain view.</b> 
            <br>Room amenities: BALCONY, AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI). 
            <br><a href=https://www.bohinj-hotel-gasperin.com/rooms-bohinj/double-room-with-balcony-and-mountain-view.html >  
            CLICK HERE for detailed description</a><br> Free parking at the hotel."""],
        
        "s": ["""<br><br><b>Manjša soba z balkonom in pogledom na gore.</b> 
            <br>Oprema sobe: BALKON, KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI.
            <br><a href= https://www.bohinj-hotel-gasperin.com/rooms-bohinj/small-double-room-with-balcony-and-mountain-view.html>
            Za več informacij KLIKNITE TU</a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br><b>Small Double Room with Balcony and Mountain view.</b> 
            <br>Room amenities: BALCONY, AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI). 
            <br><a href= https://www.bohinj-hotel-gasperin.com/rooms-bohinj/small-double-room-with-balcony-and-mountain-view.html>  
            CLICK HERE for detailed description</a><br> Free parking at the hotel."""],
        
        "d": ["""<br><br><b>Družinska soba z balkonom in pogledom na gore.</b> 
            <br>Soba ima 2 nivoja (duplex). Oprema sobe: BALKON, KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI. 
            <br><a href= https://www.bohinj-hotel-gasperin.com/rooms-bohinj/family-room-with-balcony-and-mountain-view.html>
            Za več informacij KLIKNITE TU</a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br><b>Family Room with Balcony and Mountain View.</b> 
            <br>Room has 2 levels (duplex). Room amenities: BALCONY, AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI). 
            <br><a href=https://www.bohinj-hotel-gasperin.com/rooms-bohinj/family-room-with-balcony-and-mountain-view.html>  
            CLICK HERE for detailed description</a><br> Free parking at the hotel."""],
        
        "q": ["""<br><br><b>Štiriposteljna soba z balkonom in pogledom na gore.</b> 
            <br>Oprema sobe: BALKON, KLIMA,TUŠ, WC, SAT TV, HLADILNIK, WIFI.
            <br><a href= https://www.gasperin-bohinj.com/nastanitev-gasperin-hotel-bohinj/stiriposteljna-soba-z-balkonom-in-s-pogledom-na-gore>  
            Za več informacij KLIKNITE TU</a><br>Parkiranje pred hotelom je za naše goste brezplačno.""",
            """<br><br><b>Quadruple Room with Balcony and Mountain view.</b> 
            <br>Room amenities: BALCONY, AIR CONDITION, SHOWER, WC, SAT TV, FRIDGE, WIFI). 
            <br><a href= https://www.bohinj-hotel-gasperin.com/rooms-bohinj/quadruple-room-with-balcony-and-mountain-view.html >  
            CLICK HERE for detailed description</a><br> Free parking at the hotel."""],




    }


    garancija = {
        "brez": ["""<br><br><b>POTRDITEV:</b><br>Za potrditev vaše rezervacije ne bomo zahtevali avansa.""",
                """<br><br><b>CONFIRMATION:</b><br>We will not require any advance payment for your reservation."""],
        
        "Avans": [f"""<br><br><b>POTRDITEV:</b>
            <br>Če vam ponudba ustreza, nam vašo potrditev sporočite preko e-maila. 
            <br>Potem vam pošljemo podatke za plačilo {AvansEUR} EUR avansa.
            <br><br><b>POGOJI ZA ODPOVED REZERVACIJE:</b>
            <br>-če odpoveste rezervacijo do {odpovedniRok} dni pred datumom prihoda (do {datumOdpovedniRok} do 23:59), 
            že-plačan avans vrnemo na vaš bančni račun. <br>-če odpoveste rezervacijo pozneje ali v primeru ne-prihoda, 
            že plačanega avansa ne vračamo. <br><br><b>ZAVAROVANJE REZERVACIJE:</b><br>Gostom priporočamo, 
            da pri svoji zavarovalnici sklenejo zavarovanje za primer odpovedi rezervacije.""",
            f"""<br><br><b>CONFIRMATION:</b><br>If you would like to accept our offer, please confirm your 
            reservation by e-mail including a contact mobile telephone number and approximate time of arrival.
            <br> After your confirmation we will require a {AvansEUR} EUR deposit - we will send details.
            <br><b><br>CANCELLATION POLICY:</b><br>If cancelled up to {odpovedniRok} days before date of arrival  
            (up to {datumOdpovedniRok} until 23:59), we will give you a full refund of your deposit. 
            <br>If cancelled later or in case of no-show, we will keep the total deposit paid.<br>
            <br><b>INSURANCE:</b><br>We recommend to all guests the arrangement of insurance cover with 
            their personal insurance company.<br> This can often be done for a small premium and can cover 
            cost of cancellation as well as other liabilities."""],

        "nonRef": ["""<br><br><b>POTRDITEV:</b><br>Če vam ponudba ustreza, nam vašo potrditev sporočite preko e-maila. 
            <br>Potem vam pošljemo podatke za plačilo celotne vrednosti rezervacije.
            <br><br><b>POGOJI ZA ODPOVED REZERVACIJE:</b>
            <br>Rezervacija je brez možnosti vračila denarja (non-refundable).
            <br><br><b>ZAVAROVANJE REZERVACIJE:</b><br>Gostom priporočamo, da pri svoji zavarovalnici sklenejo zavarovanje 
            za primer odpovedi rezervacije.""",
            """<br><br><b>CONFIRMATION:</b><br>If you would like to accept our offer, please confirm your 
            reservation by e-mail including a contact mobile telephone number and approximate time of arrival.
            <br>After your confirmation we will require a 100% prepayment – we will send details.<br><br><b>
            CANCELLATION POLICY:</b><br>Reservation is non-refundable (no refunds in the event of cancellation 
            or no-show).<br><br><b>INSURANCE:</b><br>We recommend to all guests the arrangement of insurance cover 
            with their personal insurance company. <br>This can often be done for a small premium and can cover 
            the cost of cancellation as well as other liabilities."""],
        
        "ccd": [f"""<br><br><b>POTRDITEV:</b><br>Če vam ponudba ustreza, sobo rezervirajte preko naše spletne strani na TEJ POVEZAVI, 
            kamor boste morali vnesli podatke iz kreditne kartice.
            <br><br><b>POGOJI ZA ODPOVED REZERVACIJE: 
            </b><br>Rezervacijo lahko odpoveste brez stroškov odpovedi do {odpovedniRok} dni pred datumom prihoda 
            (do {datumOdpovedniRok} do 23:59)<br>Če odpoveste kasneje oz. v primeru neprihoda, 
            vam zaračunamo strošek odpovedi v vrednosti ene nočitve: {strosekOdpovedi} EUR.<br><i>
            Če kreditne kartice ne uporabljate, nam to prosim sporočite, 
            da vam pošljemo bančne podatke za plačilo avansa. </i> """,
            f"""<br><br><b>CONFIRMATION:</b><br>If you would like to accept our offer, please book offered 
            room on THAT LINK, where you will input your credit card details.<br><br><b>CANCELLATION POLICY: 
            </b><br>You can cancel your reservation FREE of charge {odpovedniRok} days before arrival day 
            (till {datumOdpovedniRok} till 23:59)<br>If you will cancel later or in case of NO SHOW, we will charge
            your credit card for $strosekOdpovedi EUR.<br><i>If you don't use a credit card, we will require an 
            advance payment to secure your reservation. Bank details will be sent. </i>   <br><br> """],
    }


    footer= [f"""<br><br><b>PRIJAVA (CHECK-IN):</b>
        <br>Prijava dne $odDat je možna od 14:00 do 22:00.<br><br><b>ODJAVA (CHECK-OUT):</b>
        <br>Odjava na dan odhoda {doDat} je do 11:00.<br><br><b>SAVNA:</b>
        <br>Nudimo finsko savno. Potrebna je rezervacija. Delovni čas do 21:00. 
        Cena 15 EUR na uro za 1 do 4 oseb.
        <br><br><b>MOŽNOST KOSILA / VEČERJE:</b>
        <br><i>Naš hotel je kategoriziran kot Garni hotel, kar pomeni, da nudimo nočitev z zajtrkom. 
        Kosila in večerje ne nudimo.</i><br>
        <br>V naši neposredni bližini se nahaja 5 restavracij.
        <br><br><B>AKTIVNOSTI/STORITVE V NAŠI BLIŽINI:</b>
        <br>POLETI: Pohodništvo, kolesarjenje, kopanje v jezeru, kanjoning, plezanje, ribolov, jahanje, zipline, 
        gondola na Vogel, jadralno padalstvo...<br>Izposoja v naši bližini: čolni, kanuji, supi, 
        gorska kolesa, električna kolesa...<br>POZIMI: Smučanje na smučiščih Vogel, Soriška planina, 
        Senožeta, Pokljuka, tek na smučeh na Pokljuki, sankanje na Voglu, krpljanje, drsanje v Bohinjski Bistrici, 
        kopanje v Vodnem parku v Bohinjski Bistrici,...
        <br><br><i>Lep pozdrav,<br>Peter Gašperin</i>
        <br>____________________________________<br><h3>Hotel Gašperin Bohinj</h3><h4>Ribčev Laz 36a
        <br>4265 Bohinjsko jezero<br>Telefon: 00 386 41 540 805</h4><br>
        
        """,
        
        f""" <br><br><b>CHECK-IN:</b><br>Check in on {odDat} is possible from 14:00 till 22:00.<br>
        <br><b>CHECK-OUT:</b><br>Check out on $doDat is till 11:00.
        <br><br><b>DINING OPTIONS:</b><br>We are B&B Hotel and we don't offer dinners.
        <br>Dinner options:<br>- Within 300 m distanste from the hotel, there are 5 restaurants. 
        <br><br><B>ACTIVITIES:</b><br>SUMMER: hiking, cycling,swimming in the lake, climbing, fishing, 
        horse riding, zipline, cable car to Vogel, paragliding ...<br>Renting near our Hotel: rowing boats, 
        canooes, sup-boards, mountain bikes, electric bikes...<br>WINTER: Skiing on: Vogel, Soriska planina, 
        Senozeta, Pokljuka; Cross-country, sledging, snow-shoeing, skating, swimming in Aquapark Bohinj,...
        <br><br><i>Kind regards,<br>Peter Gasperin</i>
        <br>____________________________________<br><H3>Hotel Gasperin Bohinj</H3><h4>
        Ribcev Laz 36a<br>4265 Bohinjsko jezero<br>Mobile: 00 386 41 540 805</h4>
        """]
    
    inBeseda = ["IN", "AND"]
    aliBeseda = ["ALI", "OR"]
    skupnaCenaBeseda = ["SKUPNA CENA: ", "TOTAL PRICE: "]




    ##########################
    # SESTAVLJANJE BESEDIL ###
    ##########################
    
    # Multiroom IN in ALI

    if multiroom == True:
        if vrstaInAli == "IN":
            htmlSobeMR = ""
            skupnaCena = "0"
            for soba in range(0, len(dictPonudba["tipSobe"])):
                 # Podatki posamezne sobe
                stOdr= (dictPonudba["tipSobe"][soba][0])
                stOtr= (dictPonudba["tipSobe"][soba][1])
                if stOdr=="":
                    stOdr="0"
                if stOtr =="":
                    stOtr="0"
                stOsebSK_ = str(int(stOdr) + int(stOtr))
                TtaxSkupaj_ = str((int(stOdr)*2 + int(stOtr)*1) * stNoci)
                koncnaCena_ = dictPonudba["tipSobe"][soba][3]
                CenaBrezTTax_ =  str(float(koncnaCena_) - int(TtaxSkupaj_))
                # Teksti posamezne sobe
                sobaCena = Template(header["cena"][jezik]).substitute(stOsebSK= stOsebSK_, stNoci= stNoci, 
                                                                    CenaBrezTTax= CenaBrezTTax_, TtaxSkupaj=TtaxSkupaj_, 
                                                                    koncnaCena=koncnaCena_)
                
                skupnaCena = str(float(skupnaCena) + float(koncnaCena_))
                tekstSobe = sobeOpisi[dictPonudba["tipSobe"][soba][2]][jezik] + sobaCena
                # Združevanje tekstov vseh sob v MR
                if soba == len(dictPonudba["tipSobe"])-1:
                    htmlSobeMR = htmlSobeMR + tekstSobe + "<br><br>" + skupnaCenaBeseda[jezik] + skupnaCena + " EUR"
                else:
                    htmlSobeMR = htmlSobeMR + tekstSobe + "<br><br>" + inBeseda[jezik]
        
        elif vrstaInAli == "ALI":
            htmlSobeMR = ""
            for soba in range(0, len(dictPonudba["tipSobe"])):
                # Podatki posamezne sobe
                stOdr= (dictPonudba["tipSobe"][soba][0])
                stOtr= (dictPonudba["tipSobe"][soba][1])
                if stOdr=="":
                    stOdr="0"
                if stOtr =="":
                    stOtr="0"
                stOsebSK_ = str(int(stOdr) + int(stOtr))
                TtaxSkupaj_ = str((int(stOdr)*2 + int(stOtr)*1) * stNoci)
                koncnaCena_ = dictPonudba["tipSobe"][soba][3]
                CenaBrezTTax_ =  str(float(koncnaCena_) - int(TtaxSkupaj_))
                # Teksti posamezne sobe
                sobaCena = Template(header["cena"][jezik]).substitute(stOsebSK= stOsebSK_, stNoci= stNoci, 
                                                                    CenaBrezTTax= CenaBrezTTax_, TtaxSkupaj=TtaxSkupaj_, 
                                                                    koncnaCena=koncnaCena_)
                
                tekstSobe = sobeOpisi[dictPonudba["tipSobe"][soba][2]][jezik] + sobaCena
                # Združevanje tekstov vseh sob v MR
                if soba == len(dictPonudba["tipSobe"])-1:
                    htmlSobeMR = htmlSobeMR + tekstSobe + "<br><br>"
                else:
                    htmlSobeMR = htmlSobeMR + tekstSobe + "<br><br>" + aliBeseda[jezik]

    elif multiroom == False:
        # Podatki posamezne sobe
        stOdr= (dictPonudba["tipSobe"][0][0])
        stOtr= (dictPonudba["tipSobe"][0][1])
        if stOdr=="":
            stOdr="0"
        if stOtr =="":
            stOtr="0"
        stOsebSK_ = str(int(stOdr) + int(stOtr))
        TtaxSkupaj_ = str((int(stOdr)*2 + int(stOtr)*1) * stNoci)
        koncnaCena_ = dictPonudba["tipSobe"][soba][3]
        CenaBrezTTax_ =  str(float(koncnaCena_) - int(TtaxSkupaj_))
        
        
        sobaCena = Template(header["cena"][jezik]).substitute(stOsebSK= stOsebSK_, stNoci= stNoci, 
                                                                    CenaBrezTTax= CenaBrezTTax_, TtaxSkupaj=TtaxSkupaj_, 
                                                                    koncnaCena=koncnaCena_)
                
        tekstSobe = sobeOpisi[dictPonudba["tipSobe"][soba][2]][jezik] + sobaCena        
    
    
   # ZAKLJUČNI TEKST - SKUPNI 
    if multiroom == True:
        html = header["pozdrav"][jezik] + "<br>" + zahteve + "<br> " + header["uvod"][jezik] + htmlSobeMR + garancija[rna][jezik] + footer[jezik]

    else:
        html = header["pozdrav"][jezik] + "<br>" + zahteve + "<br>"  + header["uvod"][jezik] + tekstSobe + garancija[rna][jezik] +footer[jezik]
    

    return html

def dodatne_zahteve(jezik):
    if jezik == "SLO":
        dict_zahteve={"":"Izberi",
                      "Veseli nas, da ste nam ponovno poslali povpraševanje.": "Veseli nas", 
                      "Družinskih in štiriposteljnih sob v želenem terminu nimamo več, zato vam lahko ponudimo dvoposteljne sobe.":"4 posteljnih sob ni",
                      "V tem terminu imamo na voljo tudi cenejše sobe. Če želite, lahko pripravim ponudbo tudi za cenejšo sobo.": "tudi cenejše ",
                      "Če sta otroka starejša od 5 let, lahko ponudimo:":"Če otroci starejši od 5",
                      "Nudimo nočitev z zajtrkom, kosila in večerje pa ne.<br>Spodaj v ponudbi so navedene možnostii za večerjo oz. kosilo v naši bližini.":"Ni kosila, večerje",
                      "Ker gre za veliko skupino oseb, vas moramo opozoriti, da je v našem hotelu prepovedano izvajati privatne zabave in s tem motiti ostale goste. Če imate v planu to, prosim, da izberete drugo nastanitev.":"Skupina",
                      "Tega tipa sobe v tem terminu ne moremo ponuditi, lahko pa ponudimo:":"Nimamo tega tipa",
                      "Nudimo SKI karte Vogel s popustom. Popust velja za vsaj 2-dnevne karte. Družinskih kart ne nudimo.":"Ski karte Vogel",
                      "OPOMBA<br> Ta ponudba je za rezervacijo, ki jo je možno odpovedati.<br> V primeru, da želite ponudbo za cenejšo rezervacijo s 100% predplačilom in brez možnosti odpovedi, nam to sporočitev, da pripravimo tudi to ponudo.<br>Rezervacije brez možnosti odpovedi so v povprečju 10% cenejše.":"cenejse sobe",
                      "Postelja ima en okvir, dve žimnici in dve prešiti odeji.":"postelja-opis",
                      "Apartmajev ne nudimo. Smo garni hotel - nudimo nočitev z zajtrkom.":"apartmajev ne nudimo",
                      
                      }

    elif jezik == "GB":
        dict_zahteve= {"":"Choose",
                        "We are glad, that you decided to send us another inquiry.":"We are glad..",
                       "Minimal number of nights in that period is 3, therefore we can't prepare you an offer.":"Minumum of 3 ngt",
                       "Quadruple rooms are not available in that period. We can offer you Double rooms.":"Qadruple not avail",
                       "Because you are a big group, we must warn you, that we don't tolerate excessive noice or party-like behaviour!":"Big group",
                       "PLEASE NOTE<br>This offer is for a reservation, which is possible to cancel.<br>Please inform us, if you would like a cheaper, non-refundable offer (which requires 100% prepayment), and we will prepare you an additional offer. <br>Non-refundable offers are, on average, 10% cheaper.":"Also cheapper",
                        }

    return dict_zahteve