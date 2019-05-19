import smtplib  
import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant

def send_mail(msg, toaddr, subject = '', fromaddr = constant.WORKER_EMAIL, password = constant.WORKER_PASS):
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(fromaddr, password) 
	message = 'Subject: {}\n\n{}'.format(subject, msg)
	s.sendmail(fromaddr, toaddr, message)
	s.quit() 

def main():
	send_mail(msg = "some message", toaddr = 'constant.WORKER_EMAIL')

if __name__ == '__main__':
	main()