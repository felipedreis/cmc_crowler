import scrapy
from datetime import datetime
from dateutil.parser import parse
from cmc_crowler.items import *

class GuidelinesSpyder(scrapy.Spider):
    name="guidelines"
    base_site='http://legislativo.cmc.mg.gov.br:8080/sapl/consultas/pauta_sessao/'
    seed='http://legislativo.cmc.mg.gov.br:8080/sapl/consultas/pauta_sessao/pauta_sessao_index_html'
    
    def start_requests(self):
        yield scrapy.Request(url=self.seed, callback=self.parse)

    def parse(self, response):
        dates = response.xpath('//select').xpath('//option/text()').extract()
        dates = [parse(x.strip()) for x in  dates]
        dates = [d for d in dates if d.year >= 2017 and d.month == 8 and d.day == 15] 
        for date in dates:
            yield scrapy.Request(url=self.seed+'?dat_sessao_sel='+date.strftime('%d/%m/%Y'), callback=self.parse_session) 
    
    def parse_session(self, response):
        session_link = response.xpath('//h3/a/@href').extract_first()
        if session_link is None:
            return
        yield scrapy.Request(url=self.base_site+session_link, callback=self.parse_guidelines)

    def parse_guidelines(self, response):
        response.xpath("//div[@id='conteudo']/fieldset[3]/table/td/a/@href").extract() # links
        response.xpath("//div[@id='conteudo']/fieldset[3]/table/td/a/text()").extract() #titles
         response.xpath("//div[@id='conteudo']/fieldset[3]/table/td/a/../text()") #authors
        fieldset = response.xpath("//div[@id='conteudo']/fieldset")[2]
        rows = fieldset.xpath('//tr')
        self.log(rows)
        for row in rows:
            self.log(row.extract())
            cols = row.xpath('//td') 
            #self.log(len(cols))
            #self.log(cols[0].re(r'Autor:(\s[A-Za-z])*'))
            #item = LawProjectItem(title=cols[0].xpath('//a/text()').extract(), author=cols[0].re(r'Autor: \s*'), link=cols[0].xpath('//a/@href').extract(), 
            #        description=cols[1].xpath('//text()').extract(), status=cols[2].xpath('//text()').extract())

            #yield item
