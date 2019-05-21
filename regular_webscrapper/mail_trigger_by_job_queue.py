import imaplib, email
import getpass
import re
import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant
import logging

def check_mail(fromaddr=constant.WORKER_EMAIL, password=constant.WORKER_PASS):
    logger = getlogger('mail')            
    logger.debug("\n\n==============================================================  CHECKING/MONITORING MAIL")
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login(fromaddr, password)
    M.select() 
    from datetime import datetime, timedelta
    cutoff = datetime.today() - timedelta(days=5)
    dt = cutoff.strftime('%d-%b-%Y')
    typ, data = M.search(None, 'UNSEEN', '(SINCE %s) (OR FROM "ssethia86@gmail.com" FROM "iamkamleshrangi@gmail.com")'%(dt,))

    #importing handmade job queue functionality
    from job_queue import Job_Queue
    jobs = Job_Queue(2)
    jobs._debug = False    
    from multiprocessing import Process as Bucket
    #from threading import Thread as Bucket    
    import worker_bse_report
    import worker_keys_stats

    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])            
                email_subject = msg['subject']
                sender_data = msg['from']
                sender_name = re.findall(r'(.*)<' , sender_data)[0]
                sender_email = re.findall(r'<(.*)>' , sender_data)[0]
                body = msg.get_payload()[0].get_payload()
                if type(body) is list:
                    body = ','.join(str(v) for v in body) 

                if sender_email in [constant.SKS_EMAIL, constant.KKR_EMAIL]:
                	logger.debug("RECEIVED EMAIL FROM CLIENT: {}".format(sender_name))
                	logger.debug("sender_data: {}\nsender_name: {}\nsender_emailaddr: {}\nsubject: {}\nbody: {}".format(sender_data, sender_name, sender_email, email_subject, body))
                	sys.path.append("{}/libs".format(constant.BASEDIR))
                	if re.search(r'(?i)bse\s?report' , email_subject):
                		logger.debug("starting worker for request type: bse report!\n")
                		jobs.append(Bucket(
                    		target = worker_bse_report.Worker().run,
                    		args = [sender_name, sender_email, email_subject, body],
                    		kwargs = {},))

                	if re.search(r'(?i)keys?\s?analysis' , email_subject):
                		logger.debug("starting worker for request type: db collection keys analysis report request")
                		jobs.append(Bucket(
                			target = worker_keys_stats.Worker().run,
                			args = [sender_name, sender_email, email_subject, body],
                			kwargs = {},)
                		)
    jobs.close()
    jobs.start()

    try:
        M.close()
        M.logout()
    except imaplib.IMAP4.abort as e:
        logger.info("IMAP abort")

def getlogger(task, resume = 'False'):
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)       
    logger = logging.getLogger()    
    fileh = logging.FileHandler(constant.LOGPATH[task], 'w') if resume == 'False'else logging.FileHandler(constant.LOGPATH[task], 'a') 
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)      
    logger.handlers = [fileh]
    return logger


def main():
    check_mail()

if __name__ == '__main__':
    main()
