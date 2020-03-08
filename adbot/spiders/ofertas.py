# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse
from money_parser import price_str

from adbot.spiders.utils import Utils
from adbot.items import AdbotItem
from adbot.spiders.constants import Tags
from adbot.spiders.constants import Key


class OfertasSpider(scrapy.Spider):
    name = 'ofertas'
    allowed_domains = ['ofertas.cu']
    start_urls = [
        'http://ofertas.cu/'
    ]
    level = 0

    map_category = {
        '/c/390/pc/': [Tags.COMPUTADORAS, Tags.PC],
        '/c/391/laptop/': [Tags.COMPUTADORAS, Tags.LAPTOP],
        '/c/392/monitores/': [Tags.COMPUTADORAS, Tags.MONITORES],
        '/c/393/tablets/': [Tags.COMPUTADORAS, Tags.TABLETS],
        '/c/394/celulares-accesorios/': [Tags.COMPUTADORAS, Tags.CELURARES, Tags.ACCESORIOS],
        '/c/395/impresoras/': [Tags.COMPUTADORAS, Tags.IMPRESORAS],
        '/c/396/fotocopiadoras/': [Tags.COMPUTADORAS, Tags.FOTOCOPIADORAS],
        '/c/397/modem-red/': [Tags.COMPUTADORAS, Tags.MODEM, Tags.RED],
        '/c/399/audio/': [Tags.COMPUTADORAS, Tags.AUDIO],
        '/c/400/consolas-videojuegos/': [Tags.COMPUTADORAS, Tags.CONSOLAS, Tags.VIDEO_JUEGOS],
        '/c/401/accesorios-componentes/': [Tags.COMPUTADORAS, Tags.ACCESORIOS, Tags.COMPONENTES],
        '/c/402/centros-reparaciones/': [Tags.COMPUTADORAS, Tags.SERVICIOS, Tags.TALLER],
        '/c/403/otros/': [Tags.COMPUTADORAS, Tags.OTROS],
        '/c/406/tv/': [Tags.ELECTRODOMOESTICOS, Tags.TV],
        '/c/407/reproductores-video/': [Tags.ELECTRODOMOESTICOS, Tags.REPRODUCTORES_DE_VIDEO],
        '/c/408/lavadoras/': [Tags.ELECTRODOMOESTICOS, Tags.LAVADORAS, Tags.HOGAR],
        '/c/409/refrigeradores/': [Tags.ELECTRODOMOESTICOS, Tags.REFRIGERADORES, Tags.HOGAR],
        '/c/410/planchas/': [Tags.ELECTRODOMOESTICOS, Tags.PLANCHAS, Tags.HOGAR],
        '/c/411/cocinas/': [Tags.ELECTRODOMOESTICOS, Tags.CONINAS, Tags.HOGAR],
        '/c/412/microwaves/': [Tags.ELECTRODOMOESTICOS, Tags.MICROWAVES, Tags.HOGAR],
        '/c/413/cafeteras-electricas/': [Tags.ELECTRODOMOESTICOS, Tags.CAFETERAS_ELECTRICAS, Tags.HOGAR],
        '/c/414/taller-reparaciones/': [Tags.ELECTRODOMOESTICOS, Tags.TALLER],
        '/c/415/otros/': [Tags.ELECTRODOMOESTICOS, Tags.OTROS],

        '/c/348/alquiler/': [Tags.INMUEBLES, Tags.ALQUILER],
        '/c/349/arrendamiento/': [Tags.INMUEBLES, Tags.ARRENDAMIENTO],
        '/c/350/compra-venta-viviendas/': [Tags.INMUEBLES, Tags.COMPRA, Tags.VENTA],
        '/c/351/construccion-mantenimiento/': [Tags.INMUEBLES, Tags.MANTENIMIENTO, Tags.CONTRUCCION],
        '/c/352/garajes-estacionamientos/': [Tags.INMUEBLES, Tags.ESTACIONAMIENTOS, Tags.GARAJES],
        '/c/353/terrenos-parcelas/': [Tags.INMUEBLES, Tags.TERRENOS, Tags.PARCELAS],
        '/c/354/permutas/': [Tags.INMUEBLES, Tags.PERMUTAS],
        '/c/355/otros/': [Tags.INMUEBLES, Tags.OTROS],

        '/c/404/ofrezco/': [Tags.EMPLEO, Tags.OFREZCO],
        '/c/405/necesito/': [Tags.EMPLEO, Tags.NECESITO],
        '/c/377/domesticos/': [Tags.SERVICIOS, Tags.DOMESTICOS],
        '/c/376/cuidados-domicilio/': [Tags.SERVICIOS, Tags.DOMESTICOS, Tags.CUIDADOS_A_DOMICILIO],
        '/c/378/gastronomia/': [Tags.SERVICIOS, Tags.GASTRONOMIA],
        '/c/379/jardineria/': [Tags.SERVICIOS, Tags.JARDINERIA],
        '/c/380/organizacion-eventos/': [Tags.SERVICIOS, Tags.ORGANIZACION_DE_EVENTOS],
        '/c/381/salud-belleza/': [Tags.SERVICIOS, Tags.BELLEZA, Tags.SALUD],
        '/c/382/cursos/': [Tags.SERVICIOS, Tags.CURSOS],
        '/c/383/traduccion-edicion/': [Tags.SERVICIOS, Tags.TRADUCCION, Tags.EDICION],
        '/c/384/repasadores/': [Tags.SERVICIOS, Tags.REPASADORES],
        '/c/385/taxis/': [Tags.SERVICIOS, Tags.TAXIS, Tags.TRANSPORTE],
        '/c/386/viajes-turismo/': [Tags.SERVICIOS, Tags.VIAJES, Tags.TURISMO],
        '/c/387/mudanza/': [Tags.SERVICIOS, Tags.MUDANZA],
        '/c/388/otros/': [Tags.SERVICIOS, Tags.OTROS],

        '/c/367/autos/': [Tags.TRANSPORTE, Tags.AUTOS],
        '/c/368/camiones/': [Tags.TRANSPORTE, Tags.CAMIONES],
        '/c/369/jeep/': [Tags.TRANSPORTE, Tags.JEEP],
        '/c/370/motos/': [Tags.TRANSPORTE, Tags.MOTOS],
        '/c/371/embarcaciones/': [Tags.TRANSPORTE, Tags.EMBARCACIONES],
        '/c/372/bicicletas/': [Tags.TRANSPORTE, Tags.BICLICLETAS],
        '/c/373/partes-piezas/': [Tags.TRANSPORTE, Tags.PIEZAS, Tags.PARTES],
        '/c/374/taller/': [Tags.TRANSPORTE, Tags.SERVICIOS, Tags.TALLER],
        '/c/375/otros/': [Tags.TRANSPORTE, Tags.OTROS],

        '/c/364/ropas-zapatos-accesorios/': [Tags.MISELANEAS, Tags.ROPAS, Tags.ZAPATOS, Tags.ACCESORIOS],
        '/c/363/perfumeria-cosmeticos/': [Tags.MISELANEAS, Tags.PERFUMERIA, Tags.COSMETICOS],
        '/c/361/joyas/': [Tags.MISELANEAS, Tags.JOYAS],
        '/c/357/articulos-ninos/': [Tags.MISELANEAS, Tags.INFANTILES],

        '/c/365/muebles-decoracion/': [Tags.MISELANEAS, Tags.MUEBLES, Tags.DECORACION],
        '/c/359/articulos-hogar/': [Tags.MISELANEAS, Tags.HOGAR, Tags.ARTICULOS],

        '/c/356/arte/': [Tags.MISELANEAS, Tags.ARTE],
        '/c/358/articulos-deportivos/': [Tags.MISELANEAS, Tags.DEPORTES, Tags.ARTICULOS],

        '/c/366/otros/': [Tags.MISELANEAS, Tags.OTROS],

        '/c/360/animales-mascotas/': [Tags.MISELANEAS, Tags.ANIMALES, Tags.MASCOTAS]
    }

    def parse(self, response):
        for href in response.xpath('//ul[@class="categories"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_page,
                                 meta={'level': self.level})

    def parse_page(self, response):
        level = int(response.meta['level'])
        tags = self.parse_tags(response.request.url)
        for href in response.xpath('//div[@class="listing list-mode"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_item,
                                 meta={Key.TAGS: tags})

        if level > 0:
            n = response.xpath('//ul[@class="pagination"]//a[@title="Siguiente"]/attribute::href').extract()
            if n:
                yield scrapy.Request(response.urljoin(n[0]),
                                     callback=self.parse_page,
                                     meta={"level": level - 1})

    def parse_item(self, response):
        item = AdbotItem()

        # parse title
        item[Key.TITLE] = self.parse_title(response)

        # parse body
        item[Key.BODY] = self.parse_body(response)

        # parse from
        item[Key.FROM] = {}
        item[Key.FROM] = self.parse_from(response)

        # try parse date
        self.parse_date(response, item)

        # parse url
        item[Key.URL] = response.url

        # parse tags
        item[Key.TAGS] = response.meta[Key.TAGS]

        item[Key.META] = {}

        # try parse price
        self.parse_meta_price(response, item)

        # try parse images
        self.parse_meta_images(response, item)

        yield item

    @staticmethod
    def parse_title(response):
        title = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//h2/text()').extract()
        return Utils.join_text(title)

    @staticmethod
    def parse_from(response):
        f = {Key.NAME: Utils.join_text(
            response.xpath('//div[@class="ad-reply-options"]//p[@class="lead"]/text()').extract()),
             Key.PHONE: Utils.join_text(response.xpath('//div[@class="ad-reply-options"]//a//strong/text()').extract())}
        return f

    def parse_meta_price(self, response, item):
        xpath = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="price"]/text()').extract()
        price = {}

        if len(xpath) == 1:
            xpath = xpath[0].replace(" ", "")

            price[Key.VALUE] = float(price_str(xpath))
            price[Key.CURRENCY] = self.parse_meta_price_currency(xpath)

            item[Key.META][Key.PRICE] = price

    def parse_tags(self, url):
        for entry in self.map_category.keys():
            if url and entry in url:
                return self.map_category[entry]
        return 0

    @staticmethod
    def parse_body(response):
        body = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="ad-description"]/text()').extract()
        return Utils.join_text(body)

    @staticmethod
    def parse_meta_images(response, item):
        item[Key.META][Key.IMAGE] = []

        images = response.xpath(
            '//div[@class="row center gallery"]//div[@class="col-xs-6 col-sm-3"]//a/attribute::href').extract()
        if len(images) > 0:
            result = []
            for i in images:
                result.append("http://ofertas.cu" + i)
            item[Key.META][Key.IMAGE] = result

    @staticmethod
    def parse_meta_price_currency(price):
        if 'CUC' in price:
            return "CUC"
        elif 'CUP' in price:
            return "CUP"
        return ""

    @staticmethod
    def parse_date(response, item):
        date = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//time/attribute::datetime').extract()
        if len(date) == 1:
            date = date[0]
            item[Key.DATE] = parse(date)  # dateparser.parse(date, languages=['es'])
