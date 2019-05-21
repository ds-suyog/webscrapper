import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant
import logging
import re

class Worker:
      def run(self, sender_name, sender_email, email_subject, body):
            sys.path.append("{}/libs".format(constant.BASEDIR))
            logger = getlogger('worker_keys_stats')
            logger.debug("\n\n==============================================================  worker for keys_stats running")
            logger.debug("requestor: {}".format(sender_name))                                 
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
            logger.debug("generating report")
            logger.debug('sending report to client')
            import mymailer_with_attach as ma
            sbj = "database '{}' keys statistics report".format(dbname)
            bdy= "Hi {}, webscrapper status report is in attachment".format(sender_name)                                          
            ma.send_mail(toaddr= sender_email,fname= constant.REPORT_KEYS_FNAME, fpath= constant.REPORT_KEYS_FPATH, 
                  subject=sbj, body= bdy )
            logger.debug("report sent.\n\n")

def getlogger(task, resume = 'False'):
      logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)       
      logger = logging.getLogger()    
      fileh = logging.FileHandler(constant.LOGPATH[task], 'w') if resume == 'False'else logging.FileHandler(constant.LOGPATH[task], 'a') 
      for hdlr in logger.handlers[:]:
            logger.removeHandler(hdlr)      
      logger.handlers = [fileh]
      return logger