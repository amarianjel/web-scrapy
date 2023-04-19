
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
import scrapy


class ScrapyMapConectaMedia(scrapy.Spider):
    name = "MapConectaMedia"
    custom_settings ={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'CLOSESPIDER_PAGECOUNT': 10,
        'FEED_EXPORT_ENCODING': 'utf-8'  # Formato de la salida
    }
    allowed_domains = ['map.conectamedia.cl']  # No me salgo del dominio
    start_urls = ["https://map.conectamedia.cl/index.php/email/view?id=232800"]


    def parse(self, response):
        print(response)
        titulo = response.xpath('//table[@id="diseno2"]//td[@id="diseno2"]/text()')
        print(titulo)


        yield titulo

# Automatización
# CORRIENDO SCRAPY SIN LA TERMINAL
process = CrawlerProcess({
     'FEED_FORMAT': 'json',
     'FEED_URI': 'datos_de_salida.json'
 })
process.crawl(ScrapyMapConectaMedia)
process.start()