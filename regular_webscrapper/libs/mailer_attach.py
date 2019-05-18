import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   
def send_mail(fromaddr="myworker11@gmail.com", password="worker@MAILER#11", toaddr="ssethia86@gmail.com", fname = '', fpath = ''):
	# instance of MIMEMultipart 
	msg = MIMEMultipart() 
  
	# storing the senders email address   
	msg['From'] = fromaddr 
  
	# storing the receivers email address  
	msg['To'] = toaddr 
  
	# storing the subject  
	msg['Subject'] = "webscrapper status report"
  
	# string to store the body of the mail 
	body = "webscrapper status report is in attachment"

	# attach the body with the msg instance 
	msg.attach(MIMEText(body, 'plain')) 

	# open the file to be sent  
	attachment = open(fpath, "rb") 

	# instance of MIMEBase and named as p 
	p = MIMEBase('application', 'octet-stream') 
  
	# To change the payload into encoded form 
	p.set_payload((attachment).read()) 
  
	# encode into base64 
	encoders.encode_base64(p) 
   
	p.add_header('Content-Disposition', "attachment; filename= %s" % fname) 
  
	# attach the instance 'p' to instance 'msg' 
	msg.attach(p) 

	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
  
	# start TLS for security 
	s.starttls() 
  
	# Authentication 
	s.login(fromaddr, password) 
  
	# Converts the Multipart msg into a string 
	text = msg.as_string() 
	# sending the mail 
	s.sendmail(fromaddr, toaddr, text) 
  
	# terminating the session 
	s.quit() 

def main():
	send_mail()
print("name: ", __name__)
if __name__ == '__main__':
	main()	