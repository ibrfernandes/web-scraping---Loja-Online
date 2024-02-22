#!/usr/bin/python3.8

import scrapy
import re
from urllib.parse import urlparse, parse_qs



class QuotesSpider(scrapy.Spider):
	name = "quotes"
	start_urls = ['https://www.build.com/kohler-bathroom-faucets/c109367?facets=masterFinishes_ss:Chromes~at_installationtype_ss:Deck%20Mounted~handleType_s:Double%20Handle~handleType_s:Single%20Handle']
	page=2
	primeira_pagina = 1
	passar_proxima_pagina = 1
	ultima_pagina_coletada = 0
	links_itens=[]
	dados_para_salvar = []
	def parse(self, response):
		
		links_primeira_pagina = []
		
		# Logica para extrair links
		links = response.xpath('*//div/div[2]/div/div/div[1]/a/@href').extract()
		for link in links:
			self.links_itens.append(link)
		
		if self.primeira_pagina == 1:
			self.primeira_pagina = 0
			for link in links:
				links_primeira_pagina.append(link) 
				
			
			
		# Logica para verificar a proxima pagina
		''' 
		Nao tinha como verificar o numero de paginas antes de carregar a pagina de tal modo desenvolveu-se a logica de verificar se na ultima pagina tinha menos itens que a pagina anterior. 
		Verificou que caso carregasse a ultima pagina +1 recarregava a primeira pagina novamente. Supondo que a ultima pagina tem tantos itens como a primeira pagina e que recarregasse a primeira pagina depois da ultima, se fez necessario verificar os links da primeira pagina com todos os links das paginas adjassentes
		'''
		if self.page == 2:
			self.ultima_pagina_coletada = len(links)
			
		
		if ((links == links_primeira_pagina) and (self.page>2)) or (self.ultima_pagina_coletada > len(links)):
			self.passar_proxima_pagina = 0
		

			self.links_itens = set(self.links_itens)
			i=0
			for link in self.links_itens:
			
				new_url = "https://www.build.com" + str(link)
				yield scrapy.Request(new_url, callback=self.extrair_dados)
				
				
		# Cria um link para a pagina seguinte	e verifica se a ultima pagina ja foi alcançada	
		new_url = self.start_urls[0] + "&page=" + str(self.page)
		self.page += 1	
		if self.passar_proxima_pagina == 1:
			yield scrapy.Request(new_url, callback=self.parse)		

			
	def extrair_dados(self, response):

		model = response.xpath('//*[@id="pdp-buysection"]//section/h3/span/text()').get()
		from_the = response.xpath('//*[@id="pdp-buysection"]//section//a/span/text()').getall()
		from_the = ''.join(from_the)
		mounting_type =  response.xpath('//table/tbody/tr[td/div/span[text()="Mounting Type"]]/td[2]/text()').get()
		faucet_holes = response.xpath('//table/tbody/tr[td/div/span[text()="Faucet Holes"]]/td[2]/text()').get()
		spout_reach = response.xpath('//table/tbody/tr[td/div/span[text()="Spout Reach"]]/td[2]/text()').get()
		spout_height = response.xpath('//table/tbody/tr[td/div/span[text()="Spout Height"]]/td[2]/text()').get()
		link = response.url


		dados = [model, from_the, mounting_type, faucet_holes, spout_reach, spout_height, link]

		self.dados_para_salvar.append(dados)

			
			
			
	def closed(self, reason):

		with open('teste.csv', 'w', encoding='utf-8') as csvfile:
			for link in self.links_itens:
			 	csvfile.write(link)
			 	csvfile.write("\n")
			 	
		with open('dados_itens.csv', 'w', encoding='utf-8') as salvar_dd_itens:
			for i in range(len(self.dados_para_salvar)):
				linha = ""
				for j in range(len(self.dados_para_salvar[i])):
					if j == 0:
						linha = f"{self.dados_para_salvar[i][j]}"
					else:
						linha = f"{linha};{self.dados_para_salvar[i][j]}"
				salvar_dd_itens.write(linha)
				salvar_dd_itens.write("\n")
			 	

		
		
		
		
		
