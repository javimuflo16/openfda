import http.client
import json
headers = {'User-Agent':'http-client'}

con = http.client.HTTPSConnection('api.fda.gov')
#Con el parámetro limit acotamos a 10 resultados
con.request("GET","/drug/label.json?limit=10",None,headers)
resp = con.getresponse()
drug_utf = resp.read().decode("utf-8")
con.close()

drugs = json.loads(drug_utf)
#Creamos un bucle for que itere sobre cada uno de los campos de 'results' para obtener los id de cada medicamento
for drug in range(len(drugs['results'])):
    drug_info = drugs['results'][drug]

    id = drug_info["id"]
    print("ID: ", id)
