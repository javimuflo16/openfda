import http.client
import json
#Informacion sobre el navegador y SO desde el que se realiza la peticion
headers = {'User-Agent':'http-client'}
#A continuacion, establecemos la conexion con el api
con = http.client.HTTPSConnection('api.fda.gov')
#Lanzamos una peticion
con.request("GET","/drug/label.json",None,headers)
#Recogemos la respuesta a nuestra peticion
resp = con.getresponse()
#Decodificamos la respuesta recogida en formato json para poder manipularla
drug_utf = resp.read().decode("utf-8")
con.close()

#Tratamos el json
drugs = json.loads(drug_utf)
#Creamos una variable que contenga la informacion del campo que nos interesa: 'results'
drug_info = drugs["results"][0]
#Creamos una variable que contenga los datos del id del producto
id = drug_info["id"]
print("ID: ", id)
#Tenemos en cuenta lo que hay dentro de purpose
purpose = drug_info["purpose"][0]
print("Proposito del producto: ", purpose)
#Dentro del campo openfda recpgemos el campo del fabricante
manu = drug_info["openfda"]["manufacturer_name"]
print("Fabricante del medicamento: ", manu)