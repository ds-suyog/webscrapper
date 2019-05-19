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
                    logger.debug("sender_data: {}\nsender_name: {}\nsender_emailaddr: {}\nsubject: {}\nbody: {}".format(sender_data, sender_name, sender_email, email_subject, body ))
                    sys.path.append("{}/libs".format(constant.BASEDIR))

                    if re.search(r'(?i)bse\s?report' , email_subject):
                        logger.debug("request type: bse report request")
                        import mymailer
                        msg_ack = "Hi {}! We have received your request. We are working on it.".format(sender_name)
                        logger.debug('sending acknowledgement to client')
                        sbj = "bse report request acknowledgement"
                        mymailer.send_mail(msg_ack, sender_email, subject = sbj)
                        import time; time.sleep(5)
                        logger.debug("processing request")
                        import webscrapper as ws
                        ws.main()
                        logger = getlogger('mail', resume = 'True')
                        logger.debug("generating report")
                        import reportbse
                        reportbse.main()
                        logger.debug('sending report to client')
                        import mymailer_with_attach as ma                            
                        ma.send_mail(toaddr= sender_email,fname= constant.REPORT_BSE_FNAME, fpath= constant.REPORT_BSE_FPATH,
                            subject="bse webscrapper status report", body= "webscrapper status report is in attachment")
                        logger.debug("report sent!\n\n")

                    if re.search(r'(?i)keys?\s?analysis' , email_subject):
                        logger.debug("REQUEST TYPE: db collection keys analysis report request")
                        result = re.search(r'(?i)(?:database|db)\s?(?:\"|\')(.*)(?:\"|\')' , email_subject)
                        if result: dbname = result.group(1) 
                        import mymailer
                        msg_ack = "Hi {}! We have received your request. We are working on it.".format(sender_name)
                        logger.debug('sending acknowledgement to client')
                        ack_sbj = "database '{}' key stats report request acknowledgement".format(dbname)
                        mymailer.send_mail(msg_ack, sender_email, subject = ack_sbj)
                        import time; time.sleep(5)
                        logger.debug("processing request")
                        import keys_stats as ks
                        report_filename = ks.main(dbname)
                        logger = getlogger('mail', resume = 'True')
                        logger.debug("generating report")
                        logger.debug('sending report to client')
                        import mymailer_with_attach as ma
                        sbj = "database '{}' keys statistics report".format(dbname)
                        bdy= "Hi {}, webscrapper status report is in attachment".format(sender_name)                                          
                        ma.send_mail(toaddr= sender_email,fname= constant.REPORT_KEYS_FNAME, fpath= constant.REPORT_KEYS_FPATH, 
                            subject=sbj, body= bdy )
                        logger.debug("report sent.\n\n")
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