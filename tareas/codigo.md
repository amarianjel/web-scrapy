from numpy import append
from selenium import webdriver
import time
import pandas as pd

def direcciones():
driver = webdriver.Chrome(
'C:/Users/Abraham Marianjel/Documents/chromedriver.exe')
driver.get("https://map.conectamedia.cl/index.php/email/view?id=232806")

    arbol(driver)
    ''' driver.execute_script("window.open('');")

    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://map.conectamedia.cl/index.php/email/view?id=232807")

    arbol(driver)
    driver.switch_to.window(driver.window_handles[0])'''

def arbol(driver):
boxs = driver.find_elements_by_xpath('//_[@id="diseno1"]')
empresas = driver.find_elements_by_xpath(
'//_[@id="diseno2"][@valign="middle"]')

    boxInfo(boxs, empresas)

def boxInfo(boxs, empresas): # Importo y creo el modulo vacio
informacionTotal = [] # Excel
df = pd.DataFrame(informacionTotal)
df.to_excel('resultadoSelenium.xlsx', index=False)
i = 0
listaEmpresa = []
for empresaa in empresas:
empresa = empresaa.find_element_by_xpath('.').text
listaEmpresa.append(empresa)
print(listaEmpresa)

    for box in boxs:
        titulo = box.find_element_by_xpath('.//a').text
        medio_Fecha = box.find_element_by_xpath('.//h3/i').text
        seccion = box.find_element_by_xpath('.').text

        informacionTotal.append({
            "Empresa": listaEmpresa[i],
            "Titulo": titulo,
            "medio_Fecha": medio_Fecha,
            "Sección": seccion
        })

        print("CARGA: " + str(i) + "\t" + listaEmpresa[i] + "\t" + titulo + "\n" +
              medio_Fecha + "\n" + seccion + "\n")
        i += 1
    print("\nPÁGINA RASTREADA Y LISTA\n------------------------------------------------------------------\n")

    # Cargar y modificar el archivo
    writer = pd.ExcelWriter('resultadoSelenium.xlsx')
    df1 = pd.DataFrame(informacionTotal)
    df1.to_excel(writer, 'Página 1', index=False)
    writer.save()
    writer.close()

    # Excel
    print(df)

direcciones()
