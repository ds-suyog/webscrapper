# webscrapper     
Two Webscrappers,        
1. By using requests + beautiful soup            
2. By using Scrapy framework                  

What webscrapper does:               
1. app scraps top 10 gainers, top 10 loosers, and trending stocks from Bombay Stock Exchange(BSE)            
2. app also provides database collection's fields statistics. 

workflow:
1. App gets triggered by email from authorized clients. It reads request 'type' from email subject and body.
2. app queues jobs and process them in the background with workers (implemented both handmade job-queue and redis job-queue)        
3. current jobs-queue dashboard: rq-dashboard 
4. app stores respective logs for information and debugging purposes
5. app inserts data in mongodb respective collections. I wrote modules to generate and receive data-dumps in both .json and .bson format.		
6. app inserts data in elasticsearch too for analytic purposes       
7. app sends report through email to respective registered clients      
8. app will include django framework for dashboarding and analytic purposes    
9. maybe I will scrap more data, and throw NLP modules in there too      

Versions:         
python 3.5.2           
requests 2.21.0            
beautifulsoup4 4.7.1                
selenium 3.141.0          
elasticsearch==7.0.1               
Scrapy 1.6.0   
 
Note: webscrapper is just for experiment purpose, with no intent of stealing data from BSE         



