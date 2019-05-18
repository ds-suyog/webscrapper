import imaplib, email
#from imaplib import IMAP4
import getpass
import re


logpath = {'mail': '{}/logs/mailer.log'.format(_basedir)}
logger = self.getlogger('')            
logger.debug("\n\n=================")

#M = imaplib.IMAP4('imap.gmail.com')
M = imaplib.IMAP4_SSL('imap.gmail.com')
#M.login(getpass.getuser(), getpass.getpass())
M.login("myworker11@gmail.com", "worker@MAILER#11")
M.select()
#typ, data = M.search(None, 'ALL')  
#typ, data = M.search(None, 'UNSEEN') 

#grab the emails from "xx@gmail.com" for the last 5 days
from datetime import datetime, timedelta
today = datetime.today()
cutoff = today - timedelta(days=5)
dt = cutoff.strftime('%d-%b-%Y')

typ, data = M.search(None, 'UNSEEN', '(SINCE %s) (OR FROM "ssethia86@gmail.com" FROM "iamkamleshrangi@gmail.com")'%(dt,))
#typ, data = M.search(None, 'UNSEEN', '(SINCE %s) (FROM "iamkamleshrangi@gmail.com")'%(dt,))

# typ, msg_ids = c.search(None, '(FROM "Doug" SUBJECT "test message 2")')
#'UNSEEN FROM "someaddr@gmail.com"|UNSEEN FROM "@onedomain.com"|UNSEEN FROM "@anotherdomain.org"

#logger.debug(typ)
#logger.debug(data)

for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822)')
    #data = [(b'5 (RFC822 {4722}', b'Delivered-To: myworker11@gmail.com\.....
    #logger.debug('Message %s\n%s\n' % (num, data[0][1]))
    #logger.debug('\n ============================================ \n')

    for response_part in data:
        if isinstance(response_part, tuple):
            #msg = email.message_from_string(response_part[1])
            msg = email.message_from_bytes(response_part[1])
            #msg = email.message_from_string(response_part[1].decode("utf-8"))  #.deoode converts bytes b'' to string
            email_subject = msg['subject']
            email_from_data = msg['from']
            name = re.findall(r'(.*)<' , email_from_data)[0]
            emailaddr_client = re.findall(r'<(.*)>' , email_from_data)[0]
            
            bodytext = msg.get_payload()[0].get_payload() # bodytext class 'str' in this case

            if type(bodytext) is list:
                bodytext=','.join(str(v) for v in bodytext) 
            
            #pload = msg.get_payload(decode=True)
            #logger.debug(pload)

            logger.debug()
            logger.debug('From : ' + email_from_data)
            logger.debug("Name: {}, Emailaddr: {}".format(name, emailaddr_client))
            logger.debug('Subject: ' + email_subject)
            logger.debug("bodytext: {}".format(bodytext))

            if emailaddr_client in ['ssethia86@gmail.com', 'iamkamleshrangi@gmail.com']:
            # bodytext - use tabulate something 
                logger.debug("received email from client: {}".format(name))
                code_match = re.findall(r'(?i)report' , email_subject)[0]
                if code_match:
                    logger.debug("It's a report request")
                    import mailer
                    msg_ack = "Hi {}! We have received your request. We are on it.".format(name)
                    logger.debug('sending acknowledgement to client: {}'.format(name))
                    mailer.send_mail(subject = "report request acknowledgement", msg= msg_ack, toaddr= emailaddr_client)
                    import time
                    time.sleep(5)
                    logger.debug("processing request")
                    import keys_analysis as ka
                    report_filename = ka.main()
                    logger.debug('sending report to client: {}'.format(name))
                    import mailer_attach as ma
                    ma.send_mail(toaddr= emailaddr_client,fname= report_filename, fpath= "/home/suyog/github/data_analytics_app/{}".format(report_filename))
                    logger.debug("sent report.")

# for uid, msg in M.idle(): # yield new messages
#     logger.debug(msg)

def getlogger(self, task):
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)       
    logger = logging.getLogger()    
    fileh = logging.FileHandler(_logpath[task], 'w')
    for hdlr in logger.handlers[:]:  # remove all old handlers
        logger.removeHandler(hdlr)      
    logger.handlers = [fileh]
    return logger

M.close()
M.logout()