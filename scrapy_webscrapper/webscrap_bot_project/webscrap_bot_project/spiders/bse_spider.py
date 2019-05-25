import scrapy

class ExtractUrls(scrapy.Spider): 
    name = "extract"                 
  
    def start_requests(self): 
        urls = ['https://www.bseindia.com/', ] 
          
        for url in urls: 
            yield scrapy.Request(url = url, callback = self.parse) 

