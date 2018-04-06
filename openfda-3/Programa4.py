import http.client
import json
import http.server
import socketserver

PORT = 8014

#Vamos a crear una lista para obtener los datos de los medicamentos
def ten_drugs():
    list_drugs = [] #Inicializamos una lista vacia.
    headers = {'User-Agent': 'http-client'}

    con = http.client.HTTPSConnection('api.fda.gov')
    con.request("GET", "/drug/label.json?limit=10", None,headers)
    resp = con.getresponse()
    drug_utf = resp.read().decode("utf-8")
    con.close()
    drugs = json.loads(drug_utf)
    
     #Utilizamos un bucle 'for' que itere sobre cada uno de los campos que nos interesa:'results'
    for drug in range(len(drugs['results'])):
        medicamento = drugs['results'][drug]
        
        #Si existe el campo openfda se imprime el nombre del producto y añadimos este a la lista
        if (medicamento['openfda']):
            print('Nombre:', medicamento['openfda']['substance_name'][0])
            list_drugs.append(medicamento['openfda']['substance_name'][0])
        else:
            list_drugs.append("No se especifica el nombre del medicamento")
    return list_drugs

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        contenido = """<html>
        <head><title>Lista con los 10 medicamentos </title></head>
        <body style="background-color: pink">
        <h1> Nombres de los 10 medicamentos: </h2>"""

        lista = ten_drugs()
        for drug in lista:
            contenido += "<ul><li>" + drug + "</li></ul>" + "<br>"

        contenido += "</body></html>"

        self.wfile.write(bytes(contenido, "utf8"))
        print("File served!")
        return


# El servidor comienza a aqui
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.server_close()


