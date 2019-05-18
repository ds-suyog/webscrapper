import smtplib  

def send_mail(fromaddr="myworker11@gmail.com", password="worker@MAILER#11", subject = "", msg = "request received, processing request...", toaddr="ssethia86@gmail.com"):
	#creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
  
	# start TLS for security 
	s.starttls() 
  
	# Authentication 
	s.login(fromaddr, password) 
  
	message = msg
	message = 'Subject: {}\n\n{}'.format(subject, message)
	# for multiple receivers: replace with recvr_list, where recvr_list = ["xx@gmail.com", "yy@gmail.com"] 
	s.sendmail(fromaddr, toaddr, message)
	# s.quit() 

def main():
	send_mail()

if __name__ == '__main__':
	main()