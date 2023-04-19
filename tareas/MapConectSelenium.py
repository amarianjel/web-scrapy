from lxml import html
from posixpath import split
from bs4 import BeautifulSoup
import requests
from PIL import Image  # pip install Pillow
import io
from selenium import webdriver
import os
import pandas as pd
from re import split
from timeit import default_timer


def direcciones():
    time_Direcciones = 0
    driver = webdriver.Chrome(
        'C:/Users/Abraham Marianjel/Documents/chromedriver.exe')

    url = "https://map.conectamedia.cl/index.php/email/view?id="

    num_Pagina = 232800
    for x in range(1):
        # Calculos de Tiempo
        inicio = default_timer()

        # Visitar distintas paginas
        driver.get(url + str(int(num_Pagina) + x))
        print(url + str(int(num_Pagina) + x))
        arbol(driver)
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[x])

        # Finalizamos la consulta a la pagina 1
        fin = default_timer()
        tiempo_de_pagina = fin - inicio
        print(tiempo_de_pagina, "Segundos")
        print("Página: ", x+1)
        time_Direcciones += tiempo_de_pagina

    print("La cantidad de tiempo que se demoro fue: ",
          time_Direcciones/60, " minutos...")
    print(time_Direcciones/3600, " horas")
    print(time_Direcciones/84400, " dias")
    print(time_Direcciones/31536000, " anhos")


def arbol(driver):
    encabezados = driver.find_elements_by_xpath(
        '/html/body/center/table/tbody/tr/td')
    sitiosWebs = driver.find_elements_by_xpath(
        '/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1][@valign="middle"]')
    boxs = driver.find_elements_by_xpath(
        '/html/body/center/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]')

    boxInfo(encabezados, boxs, sitiosWebs)

    ''' imagenesCaja = driver.find_elements_by_xpath(
        '//td[@align="center"][@id="diseno2"]/table[@id="diseno2"]')
    imagenCaja(imagenesCaja) '''


def boxInfo(encabezados, boxs, sitiosWebs):
    # Excel
    informacionTotal = []
    i = 0
    empresa = ""
    listaWebs = []
    listaImagenes = []
    ##########################
    # Encabezado
    for encabezado in encabezados:
        empresa = encabezado.find_element_by_xpath(
            './table/tbody/tr[3]/td/table/tbody//td').text

        fecha_Informe = encabezado.find_element_by_xpath(
            './table/tbody/tr[2]/td/table/tbody//span').text
        fecha_Informe = split('\D+- ', fecha_Informe)

        # Cuando una página no tiene fecha
        if len(fecha_Informe) <= 1:
            fecha_Informe.append("No tiene fecha")

        link_Imagen = encabezado.find_element_by_xpath(
            './table/tbody//img').get_attribute('src')
        link_Pagina = encabezado.find_element_by_xpath(
            './a').get_attribute('href')

        informacionTotal.append({
            "Empresa": empresa,
            "Fecha de Informe": fecha_Informe[1],
            "Imagen Empresa": link_Imagen,
            "Link Pagina": link_Pagina
        })

    # Sitios
    for web in sitiosWebs:
        sitio = web.find_element_by_xpath('.').text
        try:
            link_Imagenes = web.find_element_by_xpath(
                './img').get_attribute('src')
            listaImagenes.append(link_Imagenes)
        except Exception:
            link_Imagenes = "Logo no disponible"
            listaImagenes.append(link_Imagenes)

        listaWebs.append(sitio)

    # Boxs
    for box in boxs:
        titulo = box.find_element_by_xpath('./a').text
        medio_Fecha = box.find_element_by_xpath('.//h3/i').text
        bajada = box.find_element_by_xpath('.').text

        link_Articulo = box.find_element_by_xpath('.//a').get_attribute('href')

        # Visitando la otra página con Scrapy

        # Visito la otra p+agina con request
        ''' requerimiento = requests.get(link_Articulo)
        parser = html.fromstring(requerimiento.text)
        articulo_Original = parser.xpath(
            '//div[@class="box-body"]/a/text()')
        try:
            articulo_Original = articulo_Original[0]
        except Exception:
            articulo_Original = "No posee Link de Articulo Original" '''
        # Visitando la página con BeautifulSoup - Demora menos
        requerimiento = requests.get(link_Articulo)
        soup = BeautifulSoup(requerimiento.text)
        try:
            ao = soup.find('div', class_="box-body")
            articulo_Original = ao.find('a').text
        except Exception:
            articulo_Original = "No hay"

        informacionTotal.append({
            "Sitio Web": listaWebs[i],
            "Titulo": titulo,
            "Fecha Articulo": medio_Fecha,
            "Texto de Bajada": bajada,
            "Link Logo": listaImagenes[i],
            "Link Articulo": link_Articulo,
            "Articulo Original": articulo_Original
        })

        print("CARGA: " + str(i))
        i += 1
    print("\nPÁGINA RASTREADA Y LISTA\n------------------------------------------------------------------\n")
    persistencia(informacionTotal, empresa)


def imagenCaja(imagenesCaja):
    i = 0
    for ig in imagenesCaja:
        try:
            url = ig.find_element_by_xpath(
                './/td/img').get_attribute('src')

            # con requests, hago el requerimiento a la URL de la imagen
            image_content = requests.get(url).content

            # PROCESAMIENTO DE LA IMAGEN
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            # nombre a guardar de la imagen
            file_path = 'C:/Users/Abraham Marianjel/Desktop/tareas/imaaa/' + \
                str(i) + '.jpg'
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
        except Exception as e:
            print(e)
            print("Error o NO EXISTE la imagen")
        i += 1


def persistencia(informacionTotal, empresa):
    if(os.path.exists('resultadoSelenium.xlsx')):
        try:
            # Cargar y modificar el archivo
            df = pd.DataFrame(informacionTotal)
            with pd.ExcelWriter('resultadoSelenium.xlsx', mode='a') as writer:
                df.to_excel(writer, empresa, index=False)
                print("Si existia y se agrego una nueva página")
        except Exception as e:
            print(e)
    else:
        try:
            df = pd.DataFrame(informacionTotal)
            df.to_excel('resultadoSelenium.xlsx', empresa, index=False)
            print("No exitia el archivo")
        except Exception as e:
            print(e)


direcciones()
