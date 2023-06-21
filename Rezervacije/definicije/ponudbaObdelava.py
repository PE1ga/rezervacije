from string import Template
import pandas as pd
from datetime import datetime
from . import razno
import os
from django.conf import settings


def ponudba_obdelava_Html(dict):
    status = dict[0]["status"]
    
    st_sob_v_dictu = len(dict) 
    jezik = dict[0]["jezik"]
    odDat = dict[0]["od"]
    doDat = dict[0]["do"]
    odpovedniRok = dict[0]["odpoved"]
    avansEUR = dict[0]["avans"]
    zahteve = dict[0]["zahteve"]
    sedaj = datetime.now().hour
    datumRokOdpovedi = (pd.to_datetime(odDat, format="%d.%m.%Y")- pd.Timedelta(days=int(odpovedniRok))).strftime('%d.%m.%Y')
    rna = dict[0]["rna"]
    
    
        
    # SKLIC
    if rna == "Avans" or rna == "Nonref":
        js_file = os.path.join(
                settings.BASE_DIR, 'Rezervacije//static//json//ponudbaSklic.json')
        jsonData =razno.odpriJson(js_file=js_file)
        sklic = jsonData+1
        razno.shraniJson(js_file=js_file,jsonData=sklic)
    else:
        sklic = "ni sklica"
    

    # če je četrtek ali petek, moraš preskočiti vikend, ponedeljek(7) , nedelja(6)
    st_dneva = pd.to_datetime("today").weekday()
    
    if st_dneva == 3: #četrtek  + 4 = ponedeljek (7)
        rokPlacila = (pd.to_datetime("today") + pd.Timedelta(days=4)).strftime('%d.%m.%Y')    
    elif st_dneva == 4: # petek
        rokPlacila = (pd.to_datetime("today") + pd.Timedelta(days=3)).strftime('%d.%m.%Y')    
    else:
        rokPlacila = (pd.to_datetime("today") + pd.Timedelta(days=2)).strftime('%d.%m.%Y')
    
    
    
    
    
    
    
    # Jezik
    if jezik == "SLO":
        jezik = 0
    elif jezik == "GB":
        jezik = 1
    
    # Pozdrav
    if sedaj < 12:
        pozdrav =["Dobro jutro ", "Good morning "]
    elif sedaj < 18:
        pozdrav =["Dober dan", "Good afternoon "]
    else:
        pozdrav =["Dober večer", "Good evening "]
    
    
    ####################
    ### TEXTI 1. DEL ###
    ####################
    text_cena= [("""<br><br><b>CENA:</b><br>Storitev: nočitev z zajtrkom<br>Število oseb: $stOsebSK 
                    <br>Število nočitev: $stNoci <br>Cena nastanitve: $CenaBrezTTax EUR
                    <br>Turistična taksa: $TtaxSkupaj EUR<br><b>NASTANITEV SKUPAJ: $koncnaCena EUR</b>"""),
                ("""<br><br><b>PRICE:</b><br>Service: Bed & Breakfast<br>Number of persons: $stOsebSK 
                    <br>Number of nights: $stNoci <br>Price for accommodation: $CenaBrezTTax EUR<br>
                    Tourist tax: $TtaxSkupaj EUR<br><b>ACCOMMODATION TOTAL: $koncnaCena EUR</b>  """)]

    tip_sobe ={"x": ["Economy dvoposteljna soba 12m2.","Economy double room 12m2."],
               "y":["Economy dvoposteljna podstrešna soba 12m2", "Economy Double Attic Room 12m2"],
               "f":["Dvoposteljna soba z balkonom in pogledom na gozd", "Double room with balcony and forest view"],
               "c":["Dvoposteljna soba z balkonom in pogledom na gozd", "Double room with balcony and forest view"],
               "s":["Manjša soba z balkonom in pogledom na gore", "Small double room with mountain view"],
               "g":["Dvoposteljna soba s pogledom na gore- pritličje", "Double room with mountain view- ground floor"],
               "d":["Družinska soba z balkonom in pogledom na gore", "Family room with balcony and mountain view"],
               "q":["Štiriposteljna soba z balkonom in pogledom na gore", "Quadruple room with balcony and mountain view"],
                
            
            }
    inBeseda = ["IN", "AND"]
    skupnaCenaBeseda = ["SKUPNA CENA REZERVACIJE: ", "TOTAL PRICE OF THE RESERVATION: "]


    # GLAVNI LOOP
    sobe_opis_skupni = ""
    skupna_cena_eur = ""
    for soba in range(0, st_sob_v_dictu):
        tip= dict[soba]["tip"]
        stOdr= dict[soba]["stOdr"]
        stOtr= dict[soba]["stOtr"]
        imeStranke = dict[soba]["ime"]
        koncna_cena_sobe = dict[soba]["cena"]
        # Odrasli, otroci
        if stOdr=="":
            stOdr="0"
        if stOtr =="":
            stOtr="0"
        stOsebSK_=str(int(stOdr) + int(stOtr))
        stNoci= (pd.to_datetime(doDat, format="%d.%m.%Y") - pd.to_datetime(odDat, format="%d.%m.%Y")).days
        # Ttax
        TtaxSkupaj_ = str((int(stOdr)*2 + int(stOtr)*1) * stNoci)
        
        # Cena
        CenaBrezTTax_ =  str(float(koncna_cena_sobe) - int(TtaxSkupaj_))
        # Ime sobe
        ime_sobe = tip_sobe[tip][jezik]
        
        soba_opis_trenutna = Template(text_cena[jezik]).substitute(stOsebSK= stOsebSK_, stNoci= stNoci, 
                                                        CenaBrezTTax= CenaBrezTTax_, TtaxSkupaj=TtaxSkupaj_, 
                                                        koncnaCena=koncna_cena_sobe)
        
        soba_opis_trenutna = "<b>" + ime_sobe + "</b>" + soba_opis_trenutna
         
        if st_sob_v_dictu == 1: # Edina soba . MonoRoom
            sobe_opis_skupni = soba_opis_trenutna
            skupna_cena_eur = str(koncna_cena_sobe)
        else: # MultiRoom
            if soba != st_sob_v_dictu-1: # Ni zadnja soba v loopu >> moraš vmes dati IN
                sobe_opis_skupni =sobe_opis_skupni + soba_opis_trenutna + "<br><br>" + inBeseda[jezik] + "<br><br>"
            else:
                sobe_opis_skupni = sobe_opis_skupni + soba_opis_trenutna
            
            # Skupna cena v MR
            if soba == 0: # prvi v loopu
                skupna_cena_eur = str(koncna_cena_sobe)
            else:
                skupna_cena_eur = str(float(skupna_cena_eur) + float(koncna_cena_sobe))
    
    #print(sobe_opis_skupni)
    
    strosekOdpovedi = str(round(float(skupna_cena_eur) / int(stNoci) ,0 ))
    

        
    ##################
    ## TEXTI 2. DEL ##
    ##################

    header={
        "pozdrav": [f"<h4><b>{pozdrav[jezik]} {imeStranke}!</b></h4>",
                    ],
        
        "uvod": ["<br>Hvala za potrditev rezervacije:",
                "<br>Thank you for your confirmation of your reservation:"],
        
            }
    if status =="3_Hvala":
        hvala={
            "Avans":[f"""<br><br>Prejeli smo vaše nakazilo avansa v višini {avansEUR} EUR za rezervacijo sobe:<br> <b> {tip_sobe[tip][jezik]} </b> 
                <br><br>Račun za rezervacijo vam bomo izstavili na dan odhoda {doDat}. <br>Za nakazilo se zahvaljujem.<br>
                Prijava bo možna {odDat}, od 14:00 do 22:00. Prijava <b>pred 14:00 ni možna</b>, saj do takrat čistimo in pripravljamo 
                sobe.<br><br>Na recepciji bomo za prijavo potrebovali vaše osebne dokumente.<br><br><b>PODATKI O REZERVACIJI:</b><br>""",
                
                f"""<br><br>We have received your advance payment of {avansEUR} EUR for reservation of:<br> {tip_sobe[tip][jezik]}<br><br>Your check in 
                is on {odDat}, from 14:00 till 22:00. Check-in before 14:00 is not possible. At check-in at the hotel's reception, 
                we will need your ID's.<br><br>Thank you.<br><br><b>RESERVATION DETAILS</b><br>"""],
            
            "Nonref":[f"""<br><br>Prejeli smo vaše nakazilo za rezervacijo v višini {skupna_cena_eur} EUR za rezervacijo sobe:<br> <b> 
                {tip_sobe[tip][jezik]} </b> <br><br>Račun za rezervacijo vam bomo izstavili na dan odhoda ({doDat}). <br>Za nakazilo se zahvaljujem.
                <br>Prijava bo možna {odDat}, od 14:00 do 22:00. Prijava <b>pred 14:00 ni možna</b>, saj do takrat čistimo in pripravljamo 
                sobe.<br><br>Na recepciji bomo za prijavo potrebovali vaše osebne dokumente.
                <br><br><b>PODATKI O REZERVACIJI:</b><br>""",

                f"""<br><br>Thank you- we have received your pre-payment of $SkupCena EUR for reservation of:<br> {tip_sobe[tip][jezik]}<br>
                Your check in is on {odDat}, from 14:00 till 22:00. At check-in at the hotel's reception, we will need your ID's.
                <br><br>"""],
            
            "CCD":[f"""<br><br>Prejeli smo podatke o vaši kreditni kartici za rezervacijo sobe:<br> <b> {tip_sobe[tip][jezik]}</b> <br><br>
                Prijava bo možna {odDat}, od 14:00 do 22:00. Prijava <b>pred 14:00 ni možna</b>, saj do takrat čistimo in pripravljamo 
                sobe.<br><br>Na recepciji bomo za prijavo potrebovali vaše osebne dokumente. 
                <br><br><b>PODATKI O REZERVACIJI:</b><br>""",
                
                f"""<br><br>We have received your credit card details for reservation of: <br>{tip_sobe[tip][jezik]}. <br>Your check in is on 
                {odDat}, from 14:00 till 22:00. For check-in we will need your ID's.<br><br>Thank you."""],

        }
    if status =="2_Potrjeno":    
        garancija = {"Avans": [f"""<br><br><p style=color:red><b><u>POZOR:</u><br>Za dokončno potrditev rezervacije prosim, 
                    da do: {rokPlacila} nakažete {avansEUR} EUR (AVANS) na: </p></b>Bančni račun (IBAN):<br>SI56 0762 4447 0250 016 
                    <br>SWIFT : GORESI2X   <br>Lastnik računa: Peter Gašperin, Ribčev Laz 36a, 4265 Bohinjsko jezero 
                    <br>Naslov Banke: Gorenjska banka, d.d., Bleiweisova cesta 1, 4000 Kranj, Slovenija <br><b><p 
                    style=color:blue>V polje NAMEN PLAČILA napišite: ' Rezervacija  {imeStranke}' ,<br>V polje 
                    REFERENCA napišite sklicno številko: 00-{sklic}.</p></b><br>Po prejemu nakazila vam pošljemo 
                    potrdilo o prejemu preko e-maila. <br>Račun vam izstavimo na dan odhoda.<br><br><b>
                    POGOJI ZA ODPOVED REZERVACIJE:</b><br>če odpoveste rezervacijo do {odpovedniRok} dni pred datumom 
                    prihoda (do {datumRokOdpovedi} do 23:59), že-plačan avans vrnemo na vaš bančni račun. <br>
                    če odpoveste rezervacijo pozneje ali v primeru ne-prihoda, že plačanega avansa ne vračamo.
                    <br><br><br><i>Lep pozdrav,<br>Peter Gašperin</i>
                            <br>____________________________________<br><h3>Hotel Gašperin Bohinj</h3><h4>Ribčev Laz 36a<br>
                            4265 Bohinjsko jezero<br>Telefon: 00 386 41 540 805</h4>""", 

                    f"""<br><br><b>CONFIRMATION:</b><br><p style=color:red><b>Please note:<br> We will confirm your 
                    reservation, when your deposit of {avansEUR} EUR has been paid until: {rokPlacila} to:</b></p> 
                    Bank account (IBAN):<br>SI56 0762 4447 0250 016 <br> SWIFT : GORESI2X   <br>Accont owner: 
                    Peter Gašperin, Ribčev Laz 36a, 4265 Bohinjsko jezero <br>Bank adderss: Gorenjska banka, d.d., 
                    Bleiweisova cesta 1, 4000 Kranj, Slovenija <br><br><b><p style=color:blue>Please write ' Reservation 
                    {imeStranke} ' in the field PAYMENT FOR.</p></b><br><b>CANCELLATION POLICY:</b><br>If cancelled up 
                    to {odpovedniRok} days before date of arrival (up to {datumRokOdpovedi} until 23:59), no fee will be 
                    charged. Deposit that was already paid, will be refunded on your bank account.<br>If cancelled later 
                    or in case of no-show, the TOTAL deposit will be charged.<br><br><b>INSURANCE:</b><br>We recommend to 
                    all guests the arrangement of insurance cover with their personal insurance company.<br>This can often 
                    be done for a small premium and can cover the cost of cancellation as well as other liabilities.
                    <br><br><br><i>Kind regards,<br>Peter Gasperin</i>
                    <br>____________________________________<br><H3>Hotel Gasperin Bohinj</H3><h4>Ribcev Laz 36a<br>4265 
                    Bohinjsko jezero<br>Mobile: 00 386 41 540 805</h4>"""],
                    
            "Nonref": [f"""<br><br><p style=color:red><b><u>POZOR:</u><br>Za dokončno potrditev rezervacije
                    prosim, da do:   {rokPlacila} nakažete {skupna_cena_eur} EUR na: </p></b>Bančni račun (IBAN): 
                    SI56 0762 4447 0250 016 <br>SWIFT : GORESI2X   <br>Lastnik računa: Peter Gašperin, Ribčev Laz 
                    36a, 4265 Bohinjsko jezero <br>Naslov Banke: Gorenjska banka, d.d., Bleiweisova cesta 1, 4000 
                    Kranj, Slovenija <br><b><p style=color:blue>V polje NAMEN PLAČILA napišite: ' Rezervacija  
                    {imeStranke}' ,<br>V polje REFERENCA napišite sklicno številko: 00-{sklic}.</p></b><br>Po 
                    prejemu nakazila vam pošljemo potrdilo o prejemu preko e-maila. <br>Račun vam izstavimo na 
                    dan odhoda.<br><br><b>POGOJI ZA ODPOVED REZERVACIJE:</b><br>Rezervacija je brez možnosti 
                    vračila plačila (non-refundable) <br>V primeru odpovedi ali ne-prihoda, denarja ne vračamo.
                    <br><br><br><br><br><i>Lep pozdrav,<br>Peter Gašperin</i>
                    <br>____________________________________<br><h3>Hotel Gašperin Bohinj
                    </h3><h4>Ribčev Laz 36a<br>4265 
                    Bohinjsko jezero<br>Telefon: 00 386 41 540 805</h4>""", 
                    f"""<br><br><br><b>CONFIRMATION:</b><p style=color:red><b>Please note:<br> We will confirm your 
                    reservation when your deposit of {skupna_cena_eur} EUR has been paid by {rokPlacila} to:</p></b>
                    Bank account (IBAN):<br>SI56 0762 4447 0250 016 <br> SWIFT : GORESI2X   <br>Account owner: 
                    Peter Gašperin, Ribčev Laz 36a, 4265 Bohinjsko jezero <br>Bank address: Gorenjska banka, d.d., 
                    Bleiweisova cesta 1, 4000 Kranj, Slovenija <br><br><b><p style=color:blue>Please write ' 
                    Reservation {imeStranke} ' in the field PAYMENT FOR.</p></b><br><b>CANCELLATION POLICY:</b>
                    <br>Reservation is non-refundable.<br>No refunds in the event of cancellation or no-show.
                    <br><br><b>INSURANCE:</b><br>We recommend to all guests the arrangement of insurance cover 
                    with their personal insurance company. <br>This can often be done for a small premium and 
                    can cover the cost of cancellation as well as other liabilities.<br><br><br><i>Kind regards,
                    <br>Peter Gasperin</i><br>____________________________________<br><H3>Hotel Gasperin Bohinj
                    </H3><h4>Ribcev Laz 36a<br>4265 Bohinjsko jezero<br>Mobile: 00 386 41 540 805</h4>"""],
                    
            "Brez": ["""<br><br><b>Avansa za to rezervacijo ne bomo zahtevali.</b><br><br>Prijava je možna od 14:00 
                            do 22:00. <br>Za prijavo bomo potrebovali vaše osebne dokumente.
                            <br><br><br><i>Lep pozdrav,<br>Peter Gašperin</i>
                            <br>____________________________________<br><h3>Hotel Gašperin Bohinj</h3><h4>Ribčev 
                            Laz 36a<br>4265 Bohinjsko jezero<br>Telefon: 00 386 41 540 805</h4>""",

                    """<br><br><b>We will not require advance payment for 
                    that reservation.</b><br><br><br><i>Kind regards,<br>Peter Gasperin</i>
                    <br>____________________________________<br><H3>Hotel Gasperin Bohinj</H3><h4>Ribcev Laz 
                    36a<br>4265 Bohinjsko jezero<br>Mobile: 00 386 41 540 805</h4>"""],
                    
            "CCD": [f"""<br><br><b><p style=color:red><u>POZOR:</u><br>Za dokončno potrditev vaše rezervacije 
                    danes vnesite podatke o vaši kreditni kartici v varen spletni obrazec na 
                    TEJ POVEZAVI.<br><br> <b>POGOJI ZA ODPOVED REZERVACIJE: </b><br>Rezervacijo lahko 
                    odpoveste do $odpovedniRok dni pred datumom prihoda (do {datumRokOdpovedi} do 23:59)<br>
                    Če odpoveste kasneje oz. v primeru neprihoda, vam zaračunamo strošek odpovedi v vrednosti 
                    ene nočitve: {strosekOdpovedi} EUR.</p><br><br>Če kreditne kartice nimate, vam bomo poslali 
                    številko bančnega računa, na katerega boste nakazali 100 EUR avansa.</b><br><br><br><i>
                    Lep pozdrav,<br>Peter Gašperin</i><br>____________________________________<br><h3>
                    Hotel Gašperin Bohinj</h3><h4>Ribčev Laz 36a<br>4265 Bohinjsko jezero<br>
                    Telefon: 00 386 41 540 805</h4>""", 
                    
                    f"""<br><br>Reservation details: <br><br><br><b>To confirm your reservation, please input 
                    yours credit card details in safe online form on THAT LINK, today.<br><br>CANCELLATION POLICY: 
                    </b><br>You can cancel your reservation FREE of charge {odpovedniRok} days before arrival day 
                    (till {datumRokOdpovedi} till 23:59)<br>If you will cancel later or in case of NO SHOW, we will 
                    charge your credit card for 100 EUR.</b><br><br><br><i>Kind regards,<br>Peter Gasperin</i>
                    <br>____________________________________<br><H3>Hotel Gasperin Bohinj
                    </H3><h4>Ribcev Laz 36a<br>4265 Bohinjsko jezero<br>Mobile: 00 386 41 540 805</h4>"""],

                }

    
    
    
    ##################
    ## KONČNI TEKST###
    ##################
    if status == "2_Potrjeno":
        htmlText = header["pozdrav"][0] + header["uvod"][jezik] + "<br><br>" + sobe_opis_skupni + "<br><br><h5><b>"+ skupnaCenaBeseda[jezik] + " " + skupna_cena_eur + " EUR</b></h5>" + garancija[rna][jezik]    
    elif status =="3_Hvala":
        htmlText=htmlText = header["pozdrav"][0] + hvala[rna][jezik] + sobe_opis_skupni
    #print(htmlText)    
    return htmlText, sklic, rna, rokPlacila