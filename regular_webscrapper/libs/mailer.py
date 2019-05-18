import smtplib  
import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant

def send_mail(fromaddr = constant.WORKER_EMAIL, password = constant.WORKER_PASS, subject = '', msg, toaddr):
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(fromaddr, password) 
	message = 'Subject: {}\n\n{}'.format(subject, msg)
	s.sendmail(fromaddr, toaddr, message)
	s.quit() 

def main():
	send_mail()

if __name__ == '__main__':
	main()