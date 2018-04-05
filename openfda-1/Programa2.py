import http.client
import json
#Estalecemos la cabecera User-Agent para determinar la información de la petición
headers = {'User-Agent':'http-client'}

con = http.client.HTTPSConnection('api.fda.gov')
con.request("GET","/drug/label.json?limit=10",None,headers)#Con el parámetro limit acotamos a 10 resultados
resp = con.getresponse()
drug_utf = resp.read().decode("utf-8")
con.close()

drugs = json.loads(drug_utf)
for drug in range(len(drugs['results'])):#Creamos un bucle for que itere sobre cada uno de los campos de 'results' para obtener los id de cada medicamento
    drug_info = drugs['results'][drug]

    id = drug_info["id"]
    print("ID: ", id)