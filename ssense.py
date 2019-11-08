#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import json
import time
import datetime
from dhooks import Webhook, Embed
from fake_useragent import UserAgent



hook_url = '' #webhook for slack


sku = '4184761' #Delete 5155781 Input your sku 

api = 'https://www.ssense.com/en-us/men/product/xymonitor/zyx/'+str(sku)+'.json'

#====================================================================================================================================================================================================#
#--------------------------------------------------------------------- Time -----------------------------------------------------------------------------------------------------------------------#
#====================================================================================================================================================================================================#

def random_agent():
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    return headers

def post_message(product_link,product_image,product_name,product_price,instock_list):
    hook = Webhook(hook_url)
    embed = Embed(description='',color=0x5CDBF0,timestamp='now')
    embed.set_title(title=product_name,url=product_link)
    embed.add_field(name='Price',value=product_price)
    embed.add_field(name='Stock',value='\n'.join(instock_list))
    embed.set_thumbnail(url=product_image)
    embed.set_footer(text='Ssense Monitor by zyx', icon_url='https://pbs.twimg.com/profile_images/1118878674642714624/lNXTIWNT_400x400.jpg')
    hook.send(embed=embed)

s = requests.Session()

def task():
    old_list  = []
    while True:
        product_raw_json = s.get(api,headers=random_agent())
        product_json = json.loads(product_raw_json.text)
        product_sizes = product_json['product']['sizes']
        instock_list = []
        for i in product_sizes:
            if i['inStock'] == True:
                instock_list.append(i['number'])

        difference = [c for c in instock_list if c not in old_list]

        if difference:
            product_sku = product_json['product']['sku']
            product_name = product_json['product']['name']
            product_id = product_json['product']['id']
            product_price = product_json['product']['price']['regular']
            product_link = 'https://www.ssense.com/en-us/men/product/zyx/zyx/' + str(product_id)
            product_image = 'https://img.ssensemedia.com/images/'+str(product_sku)+'_1/zyx.jpg'

            post_message(product_link,product_image,product_name,product_price,instock_list)
            print(str(datetime.datetime.now())+" Monitoring---------[ Ssense "+ str(sku) +" ]------Restock[True]")
            old_list = instock_list
        else:
            print(str(datetime.datetime.now())+" Monitoring---------[ Ssense "+ str(sku) +" ]------Restock[False]")
        time.sleep(3)
task()
