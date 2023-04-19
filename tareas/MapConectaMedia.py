from bs4 import BeautifulSoup
import requests
from scrapy.item import Field
from scrapy.item import Item
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd


class Institucion(Item):
    Nombre_Cliente_Fecha = Field()
    titulo = Field()
    Medio_Fecha = Field()
    Sección = Field()


class mapeoEmpresas(CrawlSpider):
    name = "mapeoEmpresas"
    # En settings debo colocar un numero mayor a las paginas visitadas, para que sea permitido que scrapy realice la estracción
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 11,  # Un poco alto
        'FEED_EXPORT_ENCODING': 'utf-8'  # Formato de la salida
    }

    allowed_domains = ['map.conectamedia.cl']  # No me salgo del dominio

    # Defino mi url semilla, desde donde hasta donde deseo llegar con esta función
    def urlScrapy():
        start_urls = [
            'https://map.conectamedia.cl/index.php/email/view?id=23280']
        # itero las URL Semilla para sacar cuantas paginas quiera
        for i in range(3):
            start_urls.append(
                'https://map.conectamedia.cl/index.php/email/view?id=23280' + str(i))
        return start_urls
    # url Semilla
    start_urls = urlScrapy()

    download_delay = 2

    # Regla para recorrer las páginas
    rules = (
        Rule(LinkExtractor(
            allow=r'id=23280\d+'
        ), follow=True, callback="parse"),
    )
    # limpio el texto

    def limpiarTexto(self, texto):
        nuevoTexto = texto.replace('\n', '').replace(
            '\r', '').strip()
        return nuevoTexto

    def parse(self, response):
        pagina = []
        sel = Selector(response)
        titulos = sel.xpath(
            '//table[@id="diseno2"]//td[@id="diseno2"]')  # obtengo el arbol en una lista

        for titulo in titulos:
            # Instancio la variable item
            item = ItemLoader(Institucion(), titulo)
            # Busco en el arbol que adquiri los segmentos que me interesan
            nombre = item.add_xpath(
                'Nombre_Cliente_Fecha', './/td[@id="diseno2"][@valign="middle"]/text()', MapCompose(self.limpiarTexto))
            item.add_xpath(
                'titulo', './/table[@id="diseno2"]//td[@id="diseno1"]/a/text()', MapCompose(self.limpiarTexto))
            item.add_xpath('Medio_Fecha',
                           './/h3/i/text()', MapCompose(self.limpiarTexto))
            item.add_xpath(
                'Sección', './/td[@id="diseno1"]/text()', MapCompose(self.limpiarTexto))

            #
            pagina.append({
                "Nombre_Cliente_Fecha": nombre
            })
            yield item.load_item()

        df = pd.DataFrame(pagina)
        print(df)
        df.to_csv("resultados.xlsx")
    # Función para adquirir las imagenes de una página

    """def imagenesPagina(self):
        # Imagenes con libreria BeautifulSoup
        try:
            # Solo probaré con una página, ya que se demoraba en cargar las imágenes, es posible iterar o pasar como parametro la URL-SEMILLA para obetener las imágenes de más páginas
            url_semilla = "https://map.conectamedia.cl/index.php/email/view?id=232807"
            resp = requests.get(url_semilla)  # Realizo una consulta request
            soup = BeautifulSoup(resp.text)  # Le paso la consulta como sopa

            urls = []   # Inicializo un arreglo para luego buscar en mi árbol los elementos que sean de la propiedad que escribo a continuación

            descargas = soup.find_all('img')  # Busco las imágenes
            for descarga in descargas:
                urls.append(descarga["src"])  # Agrego a la lista las imágenes

            i = 0
            for url in urls:
                # Obtengo la consulta y sigo a traves de mi lista
                r = requests.get(url, allow_redirects=True)
                file_name = './imagenes/img-holi-' + \
                    str(i) + '.jpg'    # Le pongo nombre a mis imágenes
                # paso las imágenes como archivo
                output = open(file_name, 'wb')
                output.write(r.content)  # Escribir el archivo en mi pc
                output.close()
                i += 1

        except Exception as e:
            print(e)
            print("Error del Try por las imagenes")"""


# Le da formato de salida al archivo
process = CrawlerProcess()
process.crawl(mapeoEmpresas)
process.start()
