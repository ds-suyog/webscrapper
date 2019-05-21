import git
try:
	import credentials
except:
	pass

GITBASE = git.Repo('.', search_parent_directories=True).working_tree_dir
BASEDIR = "{}/regular_webscrapper".format(GITBASE)

BASE_URL = "https://www.bseindia.com/"
URL_GAINER = "https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=gainer&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"
URL_LOOSER = "https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=loser&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"

WORKER_EMAIL = credentials.WORKER_EMAIL
WORKER_PASS = credentials.WORKER_PASS

SKS_EMAIL = credentials.SKS_EMAIL
KKR_EMAIL = credentials.KKR_EMAIL

LOGPATH = {
			'crawl': '{}/logs/crawl.log'.format(BASEDIR),
			'parse': '{}/logs/parse.log'.format(BASEDIR),
			'geckodriver': '{}/logs/geckodriver.log'.format(BASEDIR),
			'mongo': '{}/logs/mongo.log'.format(BASEDIR),
			'mail': '{}/logs/mailer.log'.format(BASEDIR),
			'worker_bse': '{}/logs/worker_bse.log'.format(BASEDIR),
			'worker_keys_stats': '{}/logs/worker_keys_stats.log'.format(BASEDIR)						
			}
GECKODRIVER_BIN = '{}/bin/geckodriver'.format(BASEDIR)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

BSE_DB = 'bse'
REPORT_BSE_FPATH = '{}/reports/report_bse.txt'.format(BASEDIR)
REPORT_BSE_FNAME = 'report_bse.txt'

REPORT_KEYS_FPATH = '{}/reports/report_keys.txt'.format(BASEDIR)
REPORT_KEYS_FNAME = 'report_keystats.txt'
