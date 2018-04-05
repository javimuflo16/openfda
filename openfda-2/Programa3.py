import http.client
import json

headers = {'User-Agent':'http-client'}

con = http.client.HTTPSConnection('api.fda.gov')
con.request("GET","/drug/label.json?limit=100&search=active_ingredient:acetylsalicylic",None,headers)#Buscamos manualmente los medicamentos comprobando el pricipio activo
resp = con.getresponse()
drug_utf = resp.read().decode("utf-8")
con.close()

drugs = json.loads(drug_utf)["results"]
for drug in drugs: #Creamos un bucle que itere sobre el json
    if drug["openfda"]:#Si el campo openfda existe imprimimos el nombre del fabricante.
        manu = drug["openfda"]["manufacturer_name"][0]
        print("El nombre del fabricante del producto es: ", manu)
    else:
        print("El producto no indica el nombre del fabricante")
