# webscrapper     
Two Webscrappers,        
1. By using requests + beautiful soup            
2. By using Scrapy framework                  

What webscrapper does:           
1. For now, I am scraping small but interesting data     
2. app scraps top 10 gainers, top 10 loosers, and trending stocks from Bombay Stock Exchange(BSE)            
3. app stores respective logs for information and debugging purposes      
4. app inserts data in mongodb collections: gainers, loosers, trending         
5. app has modules to provide data-dumps, receive data-dumps in both .json and .bson format.		
5. app inserts data in elasticsearch too for analytic purposes       
6. app will send status report through email      
7. app will queue jobs and process them in the background with workers.     
8. app will include django framework for dashboarding and analytic purposes    
9. maybe I will scrap more data, and throw NLP modules in there too      

Versions:         
python 3.5.2           
requests 2.21.0            
beautifulsoup4 4.7.1                
selenium 3.141.0          
elasticsearch==7.0.1               
Scrapy 1.6.0   
 
Note: webscrapper is just for study purpose, with no intent of stealing data           



