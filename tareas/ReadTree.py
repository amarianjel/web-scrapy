import codecs
from lxml import html

def readTree():
    ruta = 'C:/Users/abrah/OneDrive/Desktop/tareas/arbolesHTML/pagina0.html'
    i = 0

    """ file = codecs.open(ruta, 'r', 'utf-8')
    archivoHTML = file.readline()
    while archivoHTML != "":
        i += 1
        archivoHTML = file.readline()
        print(archivoHTML)
        print("lINEA ", i)
    file.close() """


    file = codecs.open(ruta, 'r', 'utf-8')

    archivoHTML = file.readline()

    ingles = archivoHTML.xpath("//h3/text()")
    print(ingles)
    




readTree()