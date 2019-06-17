# Intelligent SpyderBots #   

#### Author: Suyog K Sethia ####     

## I wrote two Intelligent Spyder Bots ##        
1. By using requests + beautiful soup            
2. By using Scrapy framework                  

## What spyder-bot does? ##
app detects email from authorized clients, interprets request-type from email subject and body, processess the required request, and sends 'tabular' report through email back to respsective clients.    

#### Sample request 1: bse report ####   
Response:  app scraps top 10 gainers, top 10 loosers, and trending stocks from Bombay Stock Exchange(BSE). App then emails back tabular report to respective clients.                 

#### Sample request 2: db 'xx' statistics report ####    
Response:  app processes database collection's keys statistics, emails back tabular report to respective clients.    

## Workflow: ##
1. App's worker detects email from authorized clients. It interprets request 'type' from email subject and body.
2. app creates and auto-syncs jobs  (implemented both handmade job-queue and redis job-queue) 
3. app processes jobs in background with workers through multithreading or multiprocessing (choice provided)
3. app's job-queue dashboard: rq-dashboard
4. app stores respective logs for information and debugging purposes
5. app inserts data in mongodb respective collections. I wrote modules to automatically generate and receive data-dumps in both .json and .bson format.
6. app also has functionality to store data in Elasticsearch indexes.
7. app sends report through email to respective registered clients.        
8. app will include django framework for dashboarding and ORM functionality, once I decide to scale app.                
9. After scaling I might integrate NLP functionality too.        

## To run  ##
setup virtual environment,
```
$source venv/bin/activate
```

install dependencies,
```
$pip install requirements.txt
```

Feed required emails in constant.py. Then simply execute one of the three scripts named mail_trigger... . If email from client is present in worker's email box, then resultant report will be emailed back. 
```
$python mail_trigger....py
```

## Mentionable Versions ##         
python 3.5.2           
requests 2.21.0            
beautifulsoup4 4.7.1                
selenium 3.141.0          
elasticsearch==7.0.1               
Scrapy 1.6.0     
redis==3.2.1    
rq==1.0    
rq-dashboard==0.5.1    

### Note: webscrapper is for experiment purpose, with no intent of stealing data from BSE         ###



