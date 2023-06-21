from django.urls import path
from . import views
# ZA STATIC_
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path(route="", view=views.index, name="index"),

     # Odhodi, menjave, pospravljanje
     path(route="pospravljanje/", view=views.PospravljanjeSob, name="Pospravljanje"),
     path(route="pospravljanje/confirm/<int:id>", view=views.PotrdiCiscenje, name="PotrdiCiscenje"),
     path(route="pospravljanje/reset/<int:id>", view=views.ResetCiscenje, name="ResetCiscenje"),
          
     # Kontrola pospravljanje
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
    
    # Obvestilo čistilkam
     # GOSTI ŠLI VEN
    path(route="pospravljanje/detajli/gosti_sli_ven/<int:id>", view=views.GostiSliVen, name="gostisosliven"),
     # GOSTI NOČEJO ČIŠČENJA
    path(route="pospravljanje/detajli/gosti_nocejo_ciscenja/<int:id>", view=views.GostiNocejoCiscenja, name="gostinocejociscenja"),
    
     # GOSTI ŠLI VEN PRIHODI
    path(route = "pospravljanje_prihodi/detajliPrihod/gosti_sli_ven_prihodi/<int:id>", view = views.GostiSliVenPrihodi, name="gostisoslivenPrihodi"),
    
      # GOSTI ŠLI VEN ZAJTRK
    path(route = "zajtrk/gosti_sli_ven/<int:id>", view = views.GostiSliVenZajtrk, name="gostisoslivenZajtrk"),
    

    # Zajtrk
    path(route="zajtrk/", view=views.Zajtrk, name="zajtrk"), 
    path(route="zajtrk/confirmZajtrk/<int:id>", view=views.PotrdiZajtrk,
         name="PotrdiZajtrk"), path(route="zajtrk/resetZajtrk/<int:id>", view=views.ResetZajtrk, name="ResetZajtrk"),
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
     ]

     # TEST FORM #####################################################################
    
    
"""
    path(route="form_home/", view = views.form_home, name ="form_home"),
    path(route="form_Avtovnos/", view= views.form_Avtovnos, name="form_Avtovnos"),
    path(route="form_vnos_rocni/", view= views.form_vnos_rocni, name="form_vnos_rocni"),
     path(route="form_vnos_izbor_sob/", view= views.form_vnos_izbor_sob, name="form_vnos_izbor_sob"),
     path(route="form_vnos_izbor_sob/form_izberiSobo", view= views.form_izberi_sobo, name="form_izberi_sobo"),
    
    #path(route="form_Avtovnos/", view= views.get_name, name="form_Avtovnos"),
    
    path(route="form_home/form_update/<int:id>", view= views.form_updated, name="form_update"),
    path(route="form_home/form_delete/<int:id>", view= views.delete_gost, name="form_delete"),
     path(route="form_graf/", view= views.form_graf, name="form_graf"),
     path(route="form_graf/update/<str:komande>", view= views.updateIzGrafa, name="update_from_graf"),
    
    
    
    #### READ FILES
     path('readfile', views.readfile),  
    
     ]

     """