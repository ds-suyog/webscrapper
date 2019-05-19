from pymongo import MongoClient
import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant
import logging
from datetime import datetime

class Generate:
    def getmongoclient(self, dbname):
        try: 
            myclient = MongoClient(constant.MONGODB_HOST, constant.MONGODB_PORT, unicode_decode_error_handler='ignore') 
        except:   
            pass
        mydb = myclient[dbname]
        return myclient, mydb

    def get_coll_keys_stats(self, dbname):          
        myclient, mydb = self.getmongoclient(dbname)    
        colls = mydb.list_collection_names()
        for collname in colls:
            self.get_keys_stats(dbname, collname)

    def get_keys_stats(self, dbname, collname):
        myclient, mydb = self.getmongoclient(dbname) 
        mycoll = mydb[collname]
        all_keys = set()
        all_keystyps = set()
        all_keysstats = set()
        table_data= list()

        cursor = mycoll.find()
        for doc in cursor:
            try:
                keys = set(doc.keys())
                all_keys = all_keys.union(keys)                
                keystyps = [{(str(k), str(type(v).__name__))} for k,v in doc.items()]
                for val in keystyps:
                    all_keystyps = all_keystyps.union(set(val))
            except Exceptions as e:
                pass

        from tabulate import tabulate      
        all_keystyps = sorted(all_keystyps)
        for ky,typ in all_keystyps:
            cursor = mycoll.find()
            freq = sum([1 for doc in cursor if ky in doc])
            sample = None
            itercount = 0
            cursor = mycoll.find()
            for doc in cursor:
                itercount+=1
                if ky in doc:
                    sample = doc
                    all_keysstats.add((ky, typ, freq, str(sample)))
                    break
            table_data.append([ky, typ, freq, sample])            

        table_headrs = ["fieldname", "type", "frequency", "sample"]
        with open(constant.REPORT_KEYS_FPATH, 'a') as f:
            f.write("COLLECTION: {}".format(collname))
            f.write("\ntotal documents: {}".format(mycoll.count()))           
            f.write('\nkey stats: ')
            table = tabulate(table_data, headers=table_headrs, tablefmt='orgtbl')
            f.write("\n{}\n\n\n".format(table))  

def getlogger(task, resume = 'False'):
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)       
    logger = logging.getLogger()    
    fileh = logging.FileHandler(constant.LOGPATH[task], 'w') if resume == 'False'else logging.FileHandler(constant.LOGPATH[task], 'a') 
    for hdlr in logger.handlers[:]:
        logger.removeHandler(hdlr)      
    logger.handlers = [fileh]
    return logger
  
def main(db):
    gn = Generate()  
    with open(constant.REPORT_KEYS_FPATH, 'w') as f:
        f.write("REPORT: database {} keys statistics".format(db))
        f.write("\n[time stamp] {}\n\n".format(datetime.now().strftime("%B %d, %Y  %H:%M:%S")))
    gn.get_coll_keys_stats(db)                    

if __name__ == '__main__':
    main()



