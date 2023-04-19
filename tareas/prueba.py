import lxml.html
from re import split
from posixpath import split

etree = lxml.html.etree

# html = etree.parse ('liepin.html') # Se produce un error. Las etiquetas no aparecen en pares.

parser = etree.HTMLParser (encoding = "utf-8") # usado para leer archivos html
html = etree.parse ("C:/Users/abrah/OneDrive/Desktop/tareas/arbolesHTML/pagina0.html", parser = parser) # html es el tipo de objeto

 # result = etree.tostring (html, encoding = 'utf-8'). decode () # convert to string
i = 0


# Box
""" titulo = html.xpath('//tr/td[2]/a')
for n in titulo:
    i += 1
    print (i ,n.text)

fecha_articulo = html.xpath('//i')
for n in fecha_articulo:
    print(n.text)"""
    

# No esta completo la bajada
""" texto_de_bajada = html.xpath('//tr/td[1]//tr/td[1]//tr/td[2]/text()')
for n in texto_de_bajada:
    i += 1
    print(i , n) """

""" link_articulo = html.xpath('//tr/td[2]/a/@href')
for n in link_articulo:
    i+=1
    print(i, n) """


#//tr/td[@valign="top"]/node() para todo el arbol
# mejor para el box ('//tr/td[1]//tr/td[1]//tr/td[2]/text()')
listaImagenes = []
boxs = html.xpath('//tr/td[@valign="top"]')
for box in boxs:
    i += 1
    titulo = box.xpath('.//tr/td[2]/a/text()')
    fecha_articulo = box.xpath('.//tr/td[2]/i/text()')
    link_articulo = box.xpath('.//tr/td[2]/a/@href')
    # Ordenar
    texto_de_bajada = box.xpath('.//tr/td[2]/text()')
    print(i , titulo, fecha_articulo, link_articulo, texto_de_bajada)

    sitio = box.xpath('.//tr/td[1][@valign="middle"]/text()')
    try:
        link_imagen = box.xpath('.//img/@src')
        listaImagenes.append(link_imagen)
    except Exception:
        linkImagenes = "Logo no disponible"
        listaImagenes.append(listaImagenes)

    print(i, listaImagenes)

i = 0
encabezados = html.xpath('//td[@align="center"]')
for encabezado in encabezados:
    i += 1
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

    print(i, link_imagen)







# Paquete
""" data=html.xpath('//div[@class="job-info"]/p[@class="condition clearfix"]/span')
positions = []
pos = {"salary": "", "edu": "", "work_years": ""}
print(len(data))
for n in range(0, len(data), 3):
    pos = {"salary": data[n].text, "edu": data[n + 1].text, "work_years": data[n + 2].text}
    positions.append(pos)
    print(positions) """