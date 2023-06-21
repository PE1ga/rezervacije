from django.urls import path
from . import views
# ZA STATIC_
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path(route="", view=views.index, name="index"),

     # Odhodi, menjave, pospravljanje
     path(route="pospravljanje/", view=views.PospravljanjeSob, name="Pospravljanje"),
     path(route="pospravljanje/vpras_pred_potrd_pospr/<int:id>", view=views.vpras_pred_potrd_posp, name="vpras_pred_potrd_pospr"),
     path(route="pospravljanje/confirm/<int:id>", view=views.PotrdiCiscenje, name="PotrdiCiscenje"),
     path(route="pospravljanje/reset/<int:id>", view=views.ResetCiscenje, name="ResetCiscenje"),
          
     # Kontrola pospravljanje
     path(route="pospravljanje/vpras_pred_kontrolo_pospr/<int:id>", view=views.vprasaj_kontrola_pospr, name="vpras_pred_kontrolo_pospr"),
     path(route="pospravljanje/KontrolaConfirm/<int:id>", view=views.KontrolaPotrdi, name="KontrolaPotrdi"),
     path(route="pospravljanje/KontrolaPonovi/<int:id>", view=views.KontrolaPonovi, name="KontrolaPonovi"),
     path(route="pospravljanje/KontrolaReset/<int:id>", view=views.KontrolaReset,
          name="KontrolaReset"),


    
    # Checklista Pospravljanje
     #path(route="checklist/<int:id>", view = views.CheckLIST, name = "checklista"),
     path(route="checklist/<str>", view = views.CheckLIST, name = "checklista"),
          # Potrdi CL
     path(route="checklist/confirm/<str>", view = views.CheckLISTconfirm, name = "checlistaconfirm"),




    # Prihodi
    path(route="pospravljanje_prihodi/", view=views.PosprPrihodi, name="Pospravljanje_Prihodi"),
    path(route="pospravljanje_prihodi/confirm/<int:id>", view=views.PotrdiCiscenjePrh, name="PotrdiCiscenjeP"),
    path(route="pospravljanje_prihodi/reset/<int:id>", view=views.ResetCiscenjePrh, name="ResetCiscenjeP"),

     # Kontrola prihodi
     path(route="pospravljanje_prihodi/KontrolaConfirmPrihodi/<int:id>",view=views.KontrolaPrihodiPotrdi, name="KontrolaPotrdiPRH"),
     path(route="pospravljanje_prihodi/KontrolaPonoviPrihodi/<int:id>", view=views.KontrolaPrihodiPonovi, name="KontrolaPonoviPRH"),
     path(route="pospravljanje_prihodi/KontrolaResetPrihodi/<int:id>", view=views.KontrolaPrihodiReset, name="KontrolaResetPRH"),

     
     # Checklista Prihodi
     #path(route="checklistprihodi/<int:id>", view = views.CheckLISTPrihodi, name = "checklistaPrihodi"),
     #path(route="checklistprihodi/confirmPR/<str>", view = views.CheckLISTconfirmPrihodi, name = "checlistaconfirmPrihodi"),
         

     # OSTALO 

    # Detalji o rezervaciji
    path(route="pospravljanje/detajli/<int:id>", view=views.Detajli, name="Detajli"),
    path(route="pospravljanje_prihodi/detajliPrihod/<int:id>", view=views.DetaljiPrihod, name="detajliPrihod"),
    
     # Servis - vzdrževanje sob POŠLJI EMAIL
    path(route="pospravljanje/detajli/poslji_mail/<int:id>", view = views.DetajliEmail, name= "pospravljanjeEmail"),
    path(route="pospravljanje_prihodi/detajliPrihod/poslji_mail/<int:id>", view=views.DetajliPrhEmail, name="prihodiEmail"),
    
    # Obvestilo čistilkam ______________ V V V V V 
     # GOSTI ŠLI VEN
    path(route="pospravljanje/detajli/gosti_sli_ven/<int:id>", view=views.GostiSliVen, name="gostisosliven"),
    

     # GOSTI NOČEJO ČIŠČENJA
    path(route="pospravljanje/detajli/gosti_nocejo_ciscenja/<int:id>", view=views.GostiNocejoCiscenja, name="gostinocejociscenja"),
    
     # GOSTI ŠLI VEN PRIHODI
    path(route = "pospravljanje_prihodi/detajliPrihod/gosti_sli_ven_prihodi/<int:id>", view = views.GostiSliVenPrihodi, name="gostisoslivenPrihodi"),
    
      # GOSTI ŠLI VEN ZAJTRK
    path(route = "zajtrk/vpras_pred_potrd_sli_ven/<int:id>", view = views.vpras_pred_potrd_sli_ven, name="vpras_pred_potrd_sli_ven"),	     
    path(route = "zajtrk/gosti_sli_ven/<int:id>", view = views.GostiSliVenZajtrk, name="gostisoslivenZajtrk"),
    path(route="zajtrk/gosti_sli_ven_reset/<int:id>", view=views.GostiSliVenZajtrkReset, name="gostisoslivenZajtrkreset"),

     # SPREMENI STATUS (če gosti podaljšajo rezervacijo na dan odhoda popravi iz odhod >> pospravi)
    path(route="pospravljanje/detajli/popravi_akcija_na_pospravi/<int:id>", view=views.popravi_akcija_na_pospravi, name="popravi_akcija_na_pospravi"),
    path(route="pospravljanje/detajli/popravi_akcija_na_odhod/<int:id>", view=views.popravi_akcija_na_odhod, name="popravi_akcija_na_odhod"),
    path(route="pospravljanje/detajli/popravi_akcija_na_menjava/<int:id>", view=views.popravi_akcija_na_menjava, name="popravi_akcija_na_menjava"),
    
    
    
    # Zajtrk
    path(route="zajtrk/", view=views.Zajtrk, name="zajtrk"), 
    path(route="zajtrk/vprasaj_zajtrk_ok_1_2/<int:id>", view=views.vprasaj_zajtrk_ok_1_2, name="vprasaj_zajtrk_ok_1_2"), 
    path(route="zajtrk/confirmZajtrk/<int:id>", view=views.PotrdiZajtrk, name="PotrdiZajtrk"), 
    path(route="zajtrk/resetZajtrk/<int:id>", view=views.ResetZajtrk, name="ResetZajtrk"),
    path(route="zajtrk/confirmZajtrkPOL/<int:id>", view=views.PotrdiZajtrkPOL, name="PotrdiZajtrkPOL"),

    # Graf
    path(route="graf/", view = views.GrafZasedenost, name="Graf"),
    path(route="graf/graf_footer/", view = views.GrafFooter, name="Graf_footer"),
    
    # Prazne sobe
    path(route="prazneSobe/", view=views.PrazneSOBE, name="prazneSobe"),


    # RECEPCIJA
    path(route= "recepcija/", view= views.Recepcija , name="recepcija"),
    path(route= "recepcija/recepcija_detajli/<int:id>", view = views.RecepcijaDetajli, name="recepcijadetajli"),
    path(route= "recepcija/checkinOK/<int:id>", view=views.RecepcijaCheckInOK, name="checkinok"),


    # TEST FORM #####################################################################
    # RECEPCIAJ TV
    path(route="recep/", view=views.recep, name="recep"),
    

]
