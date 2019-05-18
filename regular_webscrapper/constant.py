import git

GITBASE = git.Repo('.', search_parent_directories=True).working_tree_dir
BASEDIR = "{}/regular_webscrapper".format(GITBASE)

BASE_URL = "https://www.bseindia.com/"
URL_GAINER = "https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=gainer&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"
URL_LOOSER = "https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype=loser&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby=all"

WORKER_EMAIL = "myworker11@gmail.com"
WORKER_PASS = "worker@MAILER#11"
SKS_EMAIL = "ssethia86@gmail.com"
KKR_EMAIL = "iamkamleshrangi@gmail.com"
logpath = {}
LOGPATH = {
			'crawl': '{}/logs/crawl.log'.format(BASEDIR),
			'parse': '{}/logs/parse.log'.format(BASEDIR),
			'geckodriver': '{}/logs/geckodriver.log'.format(BASEDIR),
			'mongo': '{}/logs/mongo.log'.format(BASEDIR),
			'mail': '{}/logs/mailer.log'.format(constant.BASEDIR)
			}
GECKODRIVER_BIN = '{}/bin/geckodriver'.format(BASEDIR)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

REPORT_BSE_PATH = '{}/reports/report_bse.txt'.format(BASEDIR)
REPORT_BSE_FNAME = 'report_bse.txt'

REPORT_KEYS_FPATH = '{}/reports/report_keys.txt'.format(BASEDIR)
REPORT_KEYS_FNAME = 'report_keys.txt'