# -*- coding: utf-8 -*-
import scrapy
import string
from dateutil.parser import parse

from adbot.items import AdbotItem


class OfertasSpider(scrapy.Spider):
    name = 'ofertas'
    allowed_domains = ['ofertas.cu']
    start_urls = [
        'http://ofertas.cu/'
    ]
    depth = 0

    map_category = {
        '/c/390/pc/': "10",
        '/c/391/laptop/': "1012",
        '/c/392/monitores/': "10",
        '/c/393/tablets/': "1011",
        '/c/394/celulares-accesorios/': "1011",
        '/c/395/impresoras/': "10",
        '/c/396/fotocopiadoras/': "10",
        '/c/397/modem-red/': "10",
        '/c/398/cd-dvd-bluray/': "10",
        '/c/399/audio/': "10",
        '/c/400/consolas-videojuegos/': "10",
        '/c/401/accesorios-componentes/': "10",
        '/c/402/centros-reparaciones/': "80",
        '/c/403/otros/': "10",
        '/c/406/tv/': "1013",
        '/c/407/reproductores-video/': "10",
        '/c/408/lavadoras/': "1014",
        '/c/409/refrigeradores/': "1014",
        '/c/410/planchas/': "1014",
        '/c/411/cocinas/': "1014",
        '/c/412/microwaves/': "1014",
        '/c/413/cafeteras-electricas/': "1014",
        '/c/414/taller-reparaciones/': "80",
        '/c/415/otros/': "1014",

        '/c/348/alquiler/': "7071",
        '/c/349/arrendamiento/': "7071",
        '/c/350/compra-venta-viviendas/': "7072",
        '/c/351/construccion-mantenimiento/': "70",
        '/c/352/garajes-estacionamientos/': "70",
        '/c/353/terrenos-parcelas/': "70",
        '/c/354/permutas/': "7073",
        '/c/355/otros/': "70",

        '/c/404/ofrezco/': "82",
        '/c/405/necesito/': "82",
        '/c/377/domesticos/': "81",
        '/c/376/cuidados-domicilio/': "81",
        '/c/378/gastronomia/': "81",
        '/c/379/jardineria/': "81",
        '/c/380/organizacion-eventos/': "81",
        '/c/381/salud-belleza/': "81",
        '/c/382/cursos/': "81",
        '/c/383/traduccion-edicion/': "81",
        '/c/384/repasadores/': "81",
        '/c/385/taxis/': "81",
        '/c/386/viajes-turismo/': "81",
        '/c/387/mudanza/': "81",
        '/c/388/otros/': "81",

        '/c/367/autos/': "60",
        '/c/368/camiones/': "60",
        '/c/369/jeep/': "60",
        '/c/370/motos/': "60",
        '/c/371/embarcaciones/': "60",
        '/c/372/bicicletas/': "60",
        '/c/373/partes-piezas/': "60",
        '/c/374/taller/': "60",
        '/c/375/otros/': "60",

        '/c/364/ropas-zapatos-accesorios/': "30",
        '/c/363/perfumeria-cosmeticos/': "30",
        '/c/361/joyas/': "30",
        '/c/357/articulos-ninos/': "30",

        '/c/365/muebles-decoracion/': "20",
        '/c/359/articulos-hogar/': "20",

        '/c/356/arte/': "40",
        '/c/358/articulos-deportivos/': "40",

        '/c/366/otros/': "90",

        '/c/360/animales-mascotas/': "50"
    }

    def parse(self, response):
        for href in response.xpath('//ul[@class="categories"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_page,
                                 meta={'level': self.depth})
        # next = response.xpath('//ul[@class="categories"]//a/attribute::href').extract()[1]
        # request = scrapy.Request(response.urljoin(next),
        #                          callback=self.parse_page,
        #                          meta={'level': self.depth})
        # yield request

    def parse_page(self, response):
        level = int(response.meta['level'])
        category = self.categorize(response.request.url)
        for href in response.xpath('//div[@class="listing list-mode"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_item,
                                 meta={'category': category})

        if level > 0:
            n = response.xpath('//ul[@class="pagination"]//a[@title="Siguiente"]/attribute::href').extract()
            if n:
                yield scrapy.Request(response.urljoin(n[0]),
                                     callback=self.parse_page,
                                     meta={"level": level - 1})

    def parse_item(self, response):
        item = AdbotItem()
        item['title'] = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//h2/text()').extract()
        # item['body'] = '\n'.join(response.xpath(
        #     '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="ad-description"]/text()').extract())

        item['body'] = self.parse_body(response)

        item['price'] = {}

        price = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="price"]/text()').extract()

        if len(price) == 1:
            price = price[0].split(" ")
            item['price']['value'] = float(price[0].replace("$", "").replace(",", "."))
            item['price']['currency'] = price[1]

        date = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//time/attribute::datetime').extract()
        if len(date) == 1:
            date = date[0]
            item['date'] = parse(date)  # dateparser.parse(date, languages=['es'])

        item['contact'] = {}
        item['contact']['name'] = response.xpath('//div[@class="ad-reply-options"]//p[@class="lead"]/text()').extract()
        item['contact']['phone'] = response.xpath('//div[@class="ad-reply-options"]//a//strong/text()').extract()

        item['images'] = self.parse_images(response)

        item['url'] = response.url
        item['category'] = response.meta['category']

        yield item

    def categorize(self, url):
        for entry in self.map_category.keys():
            if url and entry in url:
                return self.map_category[entry]
        return 0

    def parse_body(self, response):

        # s = "some\x00string. with\x15 funny characters"
        #
        # printable = set(string.printable)
        # filter(lambda x: x in printable, s)

        body = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="ad-description"]/text()').extract()
        result = ""
        for item in body:
            s = item

            printable = set(string.printable)
            filter(lambda x: x in printable, s)
            result += s + "\n"

        return result

    def parse_images(self, response):
        images = response.xpath(
            '//div[@class="row center gallery"]//div[@class="col-xs-6 col-sm-3"]//a/attribute::href').extract()
        result = []
        for item in images:
            result.append("http://ofertas.cu" + item)
        return result
