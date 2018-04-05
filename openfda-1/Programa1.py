import http.client
import json
#Establecemos la cabecera User-Agent para determinar la informacion de la peticion
headers = {'User-Agent':'http-client'}
#A continuacion, establecemos la conexion con el api
con = http.client.HTTPSConnection('api.fda.gov')
con.request("GET","/drug/label.json",None,headers)#Lanzamos una peticion
resp = con.getresponse()#Recogemos la respuesta a nuestra peticion
drug_utf = resp.read().decode("utf-8")#Decodificamos la respuesta recogida en formato json para poder manipularla
con.close()

drugs = json.loads(drug_utf)#Tratamos el json
drug_info = drugs["results"][0]#Creamos una variable que contenga la informacion del campo que nos interesa: 'results'
id = drug_info["id"]#Creamos una variable que contenga los datos del id del producto
print("ID: ", id)
purpose = drug_info["purpose"][0]#Tenemos en cuenta lo que hay dentro de purpose
print("Proposito del producto: ", purpose)
manu = drug_info["openfda"]["manufacturer_name"]#Dentro del campo openfda recpgemos el campo del fabricante
print("Fabricante del producto: ", manu)
