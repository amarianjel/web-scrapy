from timeit import default_timer
import requests


def direcciones():
    time_Direcciones = 0

    url = "https://map.conectamedia.cl/index.php/email/view?id="

    num_Pagina = 232800
    for x in range(1):
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
    print("La cantidad de tiempo que se demoro fue: ", time_Direcciones, " segundos...")
    print((time_Direcciones/60), " minutos")
    print((time_Direcciones/60)/60, " horas")
    print(((time_Direcciones/60)/60)/24, " dias")
    print((((time_Direcciones/60)/60)/24)/365, " anhos")


def saveTree(contenidoWeb, pagina):
    ruta = 'C:/Users/abrah/OneDrive/Desktop/tareas/arbolesHTML/pagina' + \
        str(pagina) + '.html'
    with open(ruta, 'w', encoding='utf-8') as file:
        file.writelines(str(contenidoWeb))





direcciones()
