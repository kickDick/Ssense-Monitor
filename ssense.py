#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests,threading,random
import json
import re
import time
import datetime
import random
from discord_webhook import DiscordEmbed, DiscordWebhook

hook_url = '' #webhook for slack


sku = '5155781' #Delete 5155781 Input your sku 



def getAPI(sku):
	API = 'https://www.ssense.com/en-us/men/product/zyx/zyx/'+sku+'.json'
	return API

USER_AGENT =['Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
		]

#====================================================================================================================================================================================================#
#--------------------------------------------------------------------- Time -----------------------------------------------------------------------------------------------------------------------#
#====================================================================================================================================================================================================#

def gettime():
	now = str(datetime.datetime.now())
	
	now = now.split(' ')[1]
	
	threadname = threading.currentThread().getName()
	
	threadname = str(threadname).replace('Thread', 'Task')
	
	now = '[' + str(now) + ']' + '[' + str(threadname) + ']'

	return now

def message_post(itme_name,link,sizelist,price,item_image):
	webhook = DiscordWebhook(url=hook_url,content='')
	embed = DiscordEmbed(title=itme_name,url=link,color=0x00fea9)
	embed.add_embed_field(name='Price', value=price)
	embed.add_embed_field(name='Stock', value="\n".join(sizelist))
	embed.set_thumbnail(url=str(item_image+'?wid=300&hei=300&fmt=png-alpha'))
	embed.set_footer(text='Ssense Monitor by zyx', icon_url='https://pbs.twimg.com/profile_images/1118878674642714624/lNXTIWNT_400x400.jpg')
	embed.set_timestamp()
	webhook.add_embed(embed)
	webhook.execute()



def main(sku):
	LastList = []
	while True:
		API = getAPI(sku)
		try:

			user_agent = random.choice(USER_AGENT)
			
			headers = {
			'User-Agent': user_agent
			}

			response = requests.get(API,headers=headers)
			print(response)

			
			page = json.loads(response.text)
						
			sizes = page['product']['sizes']
			
			sizelist = []
			
			sizes_sku =[]
			
			for i in range(len(sizes)):
				if sizes[i]['inStock'] == True:
				
					sizelist.append(sizes[i]['number'])
				
					sizes_sku.append(sizes[i]['sku'])
				else:
					pass
		except:
				print(gettime() + '[ERROR] --> Unable to Get stock or Get to the api')

		try:
			intersection = list(set(sizelist).intersection(set(LastList)))
			
			difference = list(set(sizelist).difference(set(LastList)))

			if difference:
				final_list = intersection + difference
				
				final_list.sort()
				
				LastList = final_list
				
				print(gettime() + '[Changes] --> TRUE')
			
			else:
				print(gettime() + '[RESTOCK] --> FALSE')
				
				final_list = []
		
		except:
				final_list=[]
				
				print(gettime() + '[ERROR] --> Error Compare Sizelis')
				pass

		if final_list:
			try:
				item_id = page['product']['id']
				
				itme_name = page['product']['name']
				
				sku_1 = page['product']['sku']
				
				price = page['product']['price']['regular']
				
				link = 'https://www.ssense.com/en-us/men/product/zyx/zyx/' + str(item_id)
				
				item_image = 'https://img.ssensemedia.com/images/'+str(sku_1)+'_1/zyx.jpg'
			
			except:
				print(gettime() + '[ERROR] --> Error Getting Fileds or value')

			message_post(itme_name,link,sizelist,price,item_image)

		time.sleep(3)
main(sku)