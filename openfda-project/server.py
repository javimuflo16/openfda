import http.server
import http.client
import socketserver
import json

# -- Puerto donde lanzar el servidor
PORT = 8000


# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase. Y los que
# nosotros consideremos los podemos reemplazar por los nuestros
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
#Definimos la funcion que nos servira para mostrar la pagina principal en formato HTML
#para poder visualizarla
    def pagina_principal(self):
        html="""
            <html>
                <head><title>Servidor OpenFda</title></head>
                <body style="background-color: pink">
                    <h1>OpenFDA App</h1>
                    <h3>Aqui les presentamos nuestra aplicacion OpenFda</h1>
                    <h4><SMALL><I>Elija una de las opciones</I></SMALL></h2>
                    <form method= "get" action="listDrugs"><input type = "submit" value="Lista de medicamentos"></input>
                    </form>
                    ----------------------------------------------------------------------------------------
                    <form method="get" action="searchDrug"><input type ="submit" value="Busqueda de medicamentos"><input type = "text" name="drug"></input></input>
                    </form>
                    ----------------------------------------------------------------------------------------
                    <form method= "get" action="listCompanies"><input type = "submit" value="Lista Companies"></input>
                    </form>
                    ----------------------------------------------------------------------------------------
                    <form method="get" action="searchCompany"><input type ="submit" value="Busqueda Companies"><input type = "text" name="drug"></input></input>
                    </form>
                    ----------------------------------------------------------------------------------------
                    <form method= "get" action= "listWarnings"><input type = "submit" value="Lista de advertencias"></input>
                    </form>
                </body>
            <html>"""
        return html
    #Definimos la funcion que nos perimitira mostrar las diferentes listas que solicitemos
    #en la pagina principal
    def lista_datos(self, lista):
        lista_html ="""
                                <html><head><title>OpenFDA App</title></head>
                                    <body style="background-color: pink">
                            """
        for dato in lista:
            lista_html += "<ul><li>" + dato + "</li></ul>"

        lista_html += """               <a href="/">Volver a la pagina principal</a>
                                    </body>
                                </html>
                            """
        return lista_html
    #Funcion que nos sirve para obtener los resultados del campo 'results'
    def resultados_general (self, limit=10):
        con = http.client.HTTPSConnection("api.fda.gov")
        con.request("GET", "/drug/label.json?limit=" + str(limit))
        resp = con.getresponse()
        inf = resp.read().decode("utf8")
        inf_drug = json.loads(inf)
        results = inf_drug["results"]
        return results

    def cabeceras(self):
        # La primera linea del mensaje de respuesta es el
        # status. Indicamos que OK
        self.send_response(200)
        #Cabeceras necesarias para que el cliente pueda entender el conetenido
        #que le enviamos
        self.send_header("content-type", "text/html")
        self.end_headers()
    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):
        resource = self.path.split("?")
        if len(resource) > 1:
            parametros = resource[1]
        else:
            parametros = ""

        limit = 10

        #Obtener los parámetros
        if parametros:
            partes_limite = parametros.split("=")
            if partes_limite[0] == "limit":
                limit = int(partes_limite[1])
                print("limit: {}".format(limit))

        else:
            print("NO HAY PARAMETROS")


        #Ahora, dependiendo de lo que elijamos en la pagina principal (la infor-
        #macion en la ruta) obtendremos una cosa u otra
        if self.path =="/":
            self.cabeceras()
            html = self.pagina_principal()
            self.wfile.write(bytes(html, "utf8"))
        elif "listDrugs" in self.path:
            self.cabeceras()
            drugs = []
            #Llama a la funcion resultados_general en la que tenemos todos los
            #resultados del campo'results'
            results = self.resultados_general(limit)
            #En la lista vacia que hemos creado vamos metiendo el 'generic_name'
            #si esta dentro del campo 'openfda'
            for dato in results:
                if ("generic_name" in dato["openfda"]):
                    drugs.append(dato["openfda"]["generic_name"][0])
                else:
                    drugs.append("Desconocido")
            #Llamamos a la funcion lista_datos que nos mostrara en formato HTML
            #la lista creada
            result_html = self.lista_datos (drugs)
            #Enviamos el mensaje
            self.wfile.write(bytes(result_html, "utf8"))

        #Hacemos lo mismo con 'listCompanies' y 'listWarnings'
        elif "listCompanies" in self.path:
            self.cabeceras()
            manufacturers = []
            results = self.resultados_general(limit)
            for dato in results:
                if("manufacturer_name" in dato["openfda"]):
                    manufacturers.append(dato["openfda"]["manufacturer_name"][0])
                else:
                    manufacturers.append("Desconocido")
            result_html = self.lista_datos(manufacturers)

            self.wfile.write(bytes(result_html, "utf8"))
        elif "listWarnings" in self.path:
            self.cabeceras()
            warnings = []
            results = self.resultados_general(limit)
            for dato in results:
                if ("warnings" in dato):
                    warnings.append(dato["warnings"][0])
                else:
                    warnings.append("Desconocido")
            result_html = self.lista_datos(warnings)

            self.wfile.write(bytes(result_html, "utf8"))

        #En este caso si lo que elejimos es la siguiente opcion, nos buscara todos
        #los medicamentos que tengan como 'active_ingredient' el que hemos escrito
        elif "searchDrug" in self.path:
            self.cabeceras()
            limit = 10
            drug = self.path.split("=")[1]

            drugs2 = []
            con = http.client.HTTPSConnection("api.fda.gov")
            con.request("GET", "/drug/label.json?limit=" +str(limit) + "&search=active_ingredient:" + drug)
            resp= con.getresponse()
            inf2 =  resp.read().decode("utf-8")
            inf2_drug = json.loads(inf2)
            search_drug = inf2_drug["results"]
            #Si el campo 'generic_name' del medicamento esta dentro del campo 'openfda',
            #nos mostrara este como un termino de una lista. En el caso de que no exista,
            #pondra 'Desconocido'
            for dato in search_drug:
                if ("generic_name" in dato["openfda"]):
                    drugs2.append(dato["openfda"]["generic_name"][0])
                else:
                    drugs2.append("Desconocido")

            result_html = self.lista_datos(drugs2)
            self.wfile.write(bytes(result_html, "utf8"))

        #Ocurre lo mismo con 'searchCompany' que en el apartado anterior
        elif "searchCompany" in self.path:
            self.cabeceras()
            limit= 10
            company = self.path.split("=")[1]
            manufacturers2 = []
            con = http.client.HTTPSConnection("api.fda.gov")
            con.request("GET","/drug/label.json?limit=" +str(limit) +"&search=openfda.manufacturer_name:" + company)
            resp = con.getresponse()
            inf2 = resp.read().decode("utf-8")
            inf2_drug = json.loads(inf2)
            search_company = inf2_drug["results"]
            #En este caso siempre nos va a buscar el campo 'manufacturer_name' dentro
            #del campo openfda.
            for dato in search_company:
                manufacturers2.append(dato["openfda"]["manufacturer_name"][0])
            result_html = self.lista_datos(manufacturers2)
            self.wfile.write(bytes(result_html, "utf8"))

        elif "redirect" in self.path:#Redireccion a la pagina principal
            print("Redirigimos a la pagina principal")
            self.send_response(301)
            self.send_header("Location", 'http://localhost:' +str(PORT))
            self.end_headers()
        elif "secret" in self.path:#Datos restringidos
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:#Recurso no encontrado
            self.send_error(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("Recurso no encontrado:'{}'.".format(self.path).encode())
        return

















socketserver.TCPServer.allow_reuse_address= True

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
