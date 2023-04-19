from timeit import default_timer
import requests
import lxml.html
from re import split
from posixpath import split
import os
import pandas as pd

def direcciones():
    time_Direcciones = 0

    url = "https://map.conectamedia.cl/index.php/email/view?id="

    num_Pagina = 232800
    for x in range(10):
        # Calculos de Tiempo
        inicio = default_timer()
        # Visitar distintas paginas
        ''' requerimiento = urllib.request.urlopen(url + str(int(num_Pagina) + x))
        contenidoWeb = requerimiento.read().decode('UTF-8')
        print(contenidoWeb)
        saveTree(contenidoWeb, x) '''
        requerimiento = requests.get(url + str(int(num_Pagina) + x))
        requerimiento = requerimiento.text

        #requerimiento = requerimiento.encode('UTF-8')

        # print(requerimiento)
        saveTree(requerimiento, x)
        # Finalizamos la consulta a la pagina 1
        fin = default_timer()
        tiempo_de_pagina = fin - inicio
        print(tiempo_de_pagina, "Segundos")
        print("Página: ", x+1)
        time_Direcciones += tiempo_de_pagina
    print("La cantidad de tiempo para guardar: ", time_Direcciones, " segundos...")
    print((time_Direcciones/60), " minutos")
    print((time_Direcciones/60)/60, " horas")
    print(((time_Direcciones/60)/60)/24, " dias")
    print((((time_Direcciones/60)/60)/24)/365, " anhos")
    # Leo
    inicio = default_timer()
    readTree()
    fin = default_timer()
    tiempo_de_lectura = fin - inicio
    time_Direcciones += tiempo_de_lectura
    print("\nTiempo de lectura ", tiempo_de_lectura, "Segundos")
    print("Tiempo total ", time_Direcciones, "Segundos")

    print("Tiempo estimado para las 232800 paginas: ", ((time_Direcciones*23280)/60)/60, " horas")
    print("Tiempo estimado para las 232800 paginas: ", (((time_Direcciones*23280)/60)/60)/24, " dias")



def saveTree(contenidoWeb, pagina):
    ruta = 'C:/Users/abrah/OneDrive/Desktop/tareas/arbolesHTML/pagina' + \
        str(pagina) + '.html'
    with open(ruta, 'w', encoding='utf-8') as file:
        file.writelines(str(contenidoWeb))

def readTree():
    informacionTotal = []
    empresa = ""
    etree = lxml.html.etree
    parser = etree.HTMLParser (encoding = "utf-8") # usado para leer archivos html
    html = etree.parse ("C:/Users/abrah/OneDrive/Desktop/tareas/arbolesHTML/pagina0.html", parser = parser) # html es el tipo de objeto

    i = 0
    encabezados = html.xpath('//td[@align="center"]')
    for encabezado in encabezados:
        empresa = encabezado.xpath('.//tr[3]//td[@valign="top"]/text()')
        try:
            fecha_informe = encabezado.xpath('.//tr[2]//td[@valign="top"]//span/text()')
            fecha_informe = split('\D+- ', fecha_informe)

            # Cuando una página no tiene fecha
            if len(fecha_informe) <= 1:
                fecha_informe.append("No tiene fecha")
        except Exception:
            fecha_informe.append("No tiene fecha")
        
        link_imagen = encabezado.xpath('.//img/@src')

        informacionTotal.append({
            "Empresa": empresa,
            "Fecha del Informe": fecha_informe,
            "Link Imagen": link_imagen
        })
        i += 1
        print(i, link_imagen, empresa)

    i = 0
    boxs = html.xpath('//tr/td[@valign="top"]')
    for box in boxs:
        link_imagen = ""
        titulo = box.xpath('.//tr/td[2]/a/text()')
        fecha_articulo = box.xpath('.//tr/td[2]/i/text()')
        link_articulo = box.xpath('.//tr/td[2]/a/@href')
        # Ordenar
        texto_de_bajada = box.xpath('.//tr/td[2]/text()')
        print(i , titulo, fecha_articulo, link_articulo, texto_de_bajada)

        sitio = box.xpath('.//tr/td[1][@valign="middle"]/text()')
        try:
            link_imagen = box.xpath('.//img/@src')
        except Exception:
            link_imagen = "Logo no disponible"

        informacionTotal.append({
            "Sitio Web": sitio,
            "Link Imagen": link_imagen,
            "Titulo": titulo,
            "Link al Articulo": link_articulo,
            "Fecha de Articulo": fecha_articulo,
            "Texto de Bajada": texto_de_bajada
        })
        i += 1
        print("CARGA: " + str(i))

direcciones()
