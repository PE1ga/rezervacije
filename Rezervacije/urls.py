from django.urls import path
from . import views
# ZA STATIC_
from django.conf import settings
from django.conf.urls.static import static

app_name = "rezervacije"

urlpatterns = [
path(route="form_home/", view = views.form_home, name ="form_home"),
path(route="form_Avtovnos/", view= views.form_Avtovnos, name="form_Avtovnos"),
path(route="form_Avtovnos_file/", view= views.form_Avtovnos_file, name="form_Avtovnos_file"),
path(route="form_vnos_rocni/", view= views.form_vnos_rocni, name="form_vnos_rocni"),
path(route="form_vnos_izbor_sob/", view= views.form_vnos_izbor_sob, name="form_vnos_izbor_sob"),
path(route="form_vnos_izbor_sob/form_izberiSobo", view= views.form_izberi_sobo, name="form_izberi_sobo"),
    
    #path(route="form_Avtovnos/", view= views.get_name, name="form_Avtovnos"),
    
path(route="form_home/form_update/<int:id>", view= views.updateIzSeznama, name="form_update"),
path(route="form_home/form_delete/<int:id>", view= views.delete_gost, name="form_delete"),
path(route="form_graf/", view= views.form_graf, name="form_graf"),
#path(route="form_graf/update/<str:komande>", view= views.updateIzGrafa, name="update_from_graf"),
path(route= "updateIzGrafa/<str:komande>", view= views.updateIzGrafa2, name="update_from_graf2"),

path(route="form_virtual/", view=views.virtual, name="form_virtual"),
path(route="form_virtual/podrobnosti/<int:id>", view=views.virtual_podrobno, name="form_virt_podrobno"),
path(route="form_virtual/podrobnosti/spremeniStatus/<int:id>", view= views.virtual_spremeni_status, name="virtual_spremeni_status"),

path(route="form_ponudba_faza_1/", view= views.ponudba_faza_1, name="form_ponudba_faza_1") ,
path(route="form_ponudba_faza_1/form_ponudba_faza_2", view= views.ponudba_faza_2, name="form_ponudba_faza_2"),
path(route="form_ponudba_faza_1/form_ponudba_faza_2/form_ponudba_tipSobe/<str:tip>", view= views.ponudba_tabela_sobe, name="form_ponudba_tipSobe"),
path(route="form_ponudba_shrani/", view= views.ponudba_shrani, name="form_ponudba_shrani"),
path(route="form_ponudba_predogled", view= views.ponudba_predogled, name="form_ponudba_predogled"),
path(route="form_ponudba_poslji", view= views.ponudba_poslji, name="form_ponudba_poslji"),
path(route="form_ponudba_brisi_sobo/<int:id_sobe>", view= views.ponudba_brisi_sobo, name="form_ponudba_brisi_sobo"),

path(route="form_ponudba_seznam", view= views.ponudba_seznam, name="form_ponudba_seznam"),
path(route="form_ponudba_obdelava/<int:id>", view= views.ponudba_obdelava, name="form_ponudba_obdelava"),
path(route="form_ponudba_obd_predogl", view= views.ponudba_obdelava_teksti, name="form_ponudba_obd_predogl"),
path(route="form_ponudba_obd_poslji", view= views.ponudba_obdelava_poslji, name="form_ponudba_obd_poslji"),

path(route="form_vnos_iz_ponudbe/<int:id>", view= views.ponudba_vnos_iz_ponudbe, name="form_vnos_iz_ponudbe"),


path(route="form_dashboard", view= views.dashboard, name="form_dashboard"),

path(route="form_bar", view= views.bar, name="form_bar"),

path(route="form_dn", view= views.dn_podatki, name="form_dn"),
path(route="form_dn/form_tiskanje_racuna/", view= views.tiskanje_racuna, name="form_tiskanje_racuna"),
path(route="form_dn/form_tiskanje_vingcard/", view= views.tiskanje_vingcard, name="form_tiskanje_vingcard"),








]