import scrapy
import json
import requests
import re

from .cep import read_cep
from ..items import CasasbahiaItem



class ProductSpider(scrapy.Spider):
    name = 'product'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    api_cep = 'https://pdp-api.casasbahia.com.br/api/v2/sku/1529600698/freight/seller/88259/zipcode/{}/source/CB?channel=MOBILE&orderby=price'
    api_payment = 'https://pdp-api.casasbahia.com.br/api/v2/sku/1529600698/price/source/CB?utm_medium=cpc&utm_source=gp_branding&utm_campaign=gg_brd_inst_cb_exata&sellerId=undefined&device_type=MOBILE'
    api_seller = 'https://pdp-api.casasbahia.com.br/api/v2/sellers/source/CB?sellerId=88259'
    start_urls = ['https://www.casasbahia.com.br/usado-iphone-xr-128gb-vermelho-bom-trocafone-1529600698/p/1529600698']

    def parse(self, response):
        url_images = []
        reviews = []
        list_cep = []
        breadcrumb = []
        items = CasasbahiaItem()
        response_json = json.loads(
            response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        )
        
        product = response_json['props']['initialState']['Product']['product']
        categories = product['categories']  
        
        for i in range(0, len(categories)):
            breadcrumb.append(categories[i]['description'])
        name = product['name']
        
        description = product['description']
        description = str(description).replace('<strong>', '').replace('</strong>', '')
        description = str(description).replace('<p>', '').replace('</p>', '')
        description = str(description).replace('<br>', '').replace('</br>', '')
        description = re.sub('\n','', description)
        description = re.sub('\r','', description)

        specs = product['specGroups']       

        images = (response_json['props']['initialState']['Product']['sku']['images'])
        for i in range(0, len(images)):
            url_images.append(images[i]['url'])
        
        quanty_rating = (response_json['props']['initialState']['Review']['ratingQty'])
        user_reviews = (response_json['props']['initialState']['Review']['userReviews'])

        for i in range(0, len(user_reviews)):
            reviews.append( {
                'autor':  user_reviews[i]['name'],
                'coment': user_reviews[i]['text'],
                'data':   user_reviews[i]['date'],
                'nota':   user_reviews[i]['rating']
            })

        
        for cep in read_cep():
            api_request = requests.get(self.api_cep.format(cep), headers=self.headers)
            response_cep = json.loads(api_request.content)
            cep_delivery = response_cep['options']
            dict_cep = {
                'cep':cep,
                'delivery':cep_delivery
            }
            list_cep.append(dict_cep)
        
        payment_request = requests.get(self.api_payment, headers=self.headers)
        response_payment = json.loads(payment_request.content)
    
        seller_request = requests.get(self.api_seller, headers=self.headers)
        response_seller = json.loads(seller_request.content)
        seller_cnpj = response_seller['document']
        seller_name = response_seller['corporateName']
        seller_address = response_seller['address']

        seller = {
            'seller': {
                'cnpj': seller_cnpj,
                'name': seller_name,
                'seller_addres': seller_address
            }
        }
        
        items['name'] = name
        items['description'] = description
        items['url_images'] = url_images
        items['quanty_rating'] = quanty_rating
        items['user_reviews'] = reviews
        items['delivery'] = list_cep
        items['payment_methods'] = response_payment['paymentView']
        items['breadcrumb'] = breadcrumb
        items['specs'] = specs
        items['seller'] = seller
       
        yield items