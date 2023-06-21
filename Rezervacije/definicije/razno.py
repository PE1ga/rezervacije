import json

def seznamSob(tipSobe):
    
    vseSobe = [10,11,12,20,21,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,50,51,52,99]
    c = [20,21,30,31,32,36,46,50,99]
    f = [43,34,99]
    g = [10,11,12,99]
    x = [35,38,39,45,99]
    q = [33,44,41,42,52,99]
    d = [40,99]
    s = [37,99]
    y = [51,99]

    slovar = {
    "vse": vseSobe,
    "c": c,
    "f": f,
    "g": g,
    "x": x,
    "q": q,
    "d": d,
    "s": s,
    "y": y,
      
    }

    listIzbSob = slovar.get(tipSobe)
    return listIzbSob

def odpriJson(js_file):
    with open(js_file, "r", encoding="utf-8") as f:
        return json.load(f)

def shraniJson(js_file, jsonData):
    with open(js_file, "w", encoding="utf-8") as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=4)

def ime_dneva_v_tednu(st_dneva):
    if st_dneva == 0:
        ime_dneva_datuma = "Ponedeljek" 
    elif st_dneva == 1:
        ime_dneva_datuma = "Torek"
    elif st_dneva == 2:
        ime_dneva_datuma = "Sreda"
    elif st_dneva == 3:
        ime_dneva_datuma = "Četrtek"
    elif st_dneva == 4:
        ime_dneva_datuma = "Petek"
    elif st_dneva == 5:
        ime_dneva_datuma = "Sobota"
    elif st_dneva == 6:
        ime_dneva_datuma = "Nedelja"
    
    return ime_dneva_datuma