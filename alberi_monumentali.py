import xlrd
import json


def coordconv(x):
    x = x.value
    degs = int(x.split("°")[0])
    therest = x.split("°")[1]
    frac_part = therest.split("'")
    f = float(frac_part[0])/60+float(frac_part[1].replace(',', '.'))/3600
    return degs+f

def get_alt(x):
    if not isinstance(x, float):
        x = x.split('\n')
        for y in x:
            if 'max' in y:
                x = float(y.split()[0].replace(',', '.'))
    return x


def coordsconv(x):
    return coordconv(x[0]),coordconv(x[1])


def load_workbook(book):
    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    #print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    #print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
    json_list = []
    max_alt = 0
    for rx in range(sh.nrows)[1:]:
        #print(sh.row(rx))
        l, n = coordsconv(sh.row(rx)[6:8])
        el = {
                'lat': l,
                'lng': n,
                'geo_altitude': float(sh.row(rx)[8].value),
                'n_sc': sh.row(rx)[10].value,
                'n_com': sh.row(rx)[11].value,
                'circ': sh.row(rx)[12].value,
                'h': get_alt(sh.row(rx)[13].value),
                'city': sh.row(rx)[4].value,
                }
        json_list.append(el)
        if not isinstance(el['h'], (float, int)):
            try:
                el['h'] = float(el['h'][0].replace(',', '.'))
            except Exception as e:
                print(f"unable to get height for value {el['h']}: {e}")
                el['h'] = -1
        if el['h'] > max_alt:
            max_alt = el['h']
    return json_list


#book = xlrd.open_workbook('Elenco_Piemonte247__3__V_agg.xls')
book = xlrd.open_workbook('VI_agg_Piemonte247_76__4__corretto.xls')
json_list = load_workbook(book)
book = xlrd.open_workbook('VI_agg_Friuli468_1__14__corretto.xls')
json_list += load_workbook(book)
with open('alberi_monumentali.js', 'w') as f:
    f.write("alberi = "+json.dumps(json_list))

