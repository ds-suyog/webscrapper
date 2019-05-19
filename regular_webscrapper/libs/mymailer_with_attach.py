import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant

def send_mail(toaddr, fname, fpath, subject, body, fromaddr=constant.WORKER_EMAIL, password=constant.WORKER_PASS):
	msg = MIMEMultipart()  
	msg['From'] = fromaddr  
	msg['To'] = toaddr   
	msg['Subject'] = subject
	body = body
	msg.attach(MIMEText(body, 'plain')) 

	attachment = open(fpath, "rb") 
	p = MIMEBase('application', 'octet-stream')  
	p.set_payload((attachment).read()) 
	encoders.encode_base64(p) 
	p.add_header('Content-Disposition', "attachment; filename= %s" % fname) 
	msg.attach(p) 

	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(fromaddr, password) 
	text = msg.as_string() 
	s.sendmail(fromaddr, toaddr, text)  
	s.quit() 

def main():
	send_mail()

if __name__ == '__main__':
	main()	