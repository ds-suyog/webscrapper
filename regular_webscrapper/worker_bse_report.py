import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant
import logging

class Worker:
	def run(self, sender_name, sender_email, email_subject, body):
		sys.path.append("{}/libs".format(constant.BASEDIR))
		logger = getlogger('worker_bse')            
		logger.debug("\n\n==============================================================  worker for bse running")
		logger.debug("requestor: {}".format(sender_name))
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
		logger.debug("generating report")
		import reportbse
		reportbse.main()
		logger.debug('sending report to client')
		import mymailer_with_attach as ma                            
		ma.send_mail(toaddr= sender_email,fname= constant.REPORT_BSE_FNAME, fpath= constant.REPORT_BSE_FPATH,
		subject="bse webscrapper status report", body= "webscrapper status report is in attachment")
		logger.debug("report sent!\n\n")

def getlogger(task, resume = 'False'):
	logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
	logger = logging.getLogger()
	fileh = logging.FileHandler(constant.LOGPATH[task], 'w') if resume == 'False'else logging.FileHandler(constant.LOGPATH[task], 'a')
	for hdlr in logger.handlers[:]:
		logger.removeHandler(hdlr)
	logger.handlers = [fileh]
	return logger
