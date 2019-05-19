from pymongo import MongoClient
import git, sys; sys.path.append("{}/regular_webscrapper".format(git.Repo('.', search_parent_directories=True).working_tree_dir))
import constant
from datetime import datetime

class Generate:
    def getmongoclient(self, dbname):
        try: 
            myclient = MongoClient(constant.MONGODB_HOST, constant.MONGODB_PORT, unicode_decode_error_handler='ignore') 
        except:   
            pass
        mydb = myclient[dbname]
        return myclient, mydb

    def all_coll_report(self, dbname):
        myclient, mydb = self.getmongoclient(dbname)    
        colls = mydb.list_collection_names()     
        for collname in colls:
            self.single_coll_report(dbname, collname)

    def single_coll_report(self, dbname, colname):
        myclient, mydb = self.getmongoclient(dbname) 
        mycol = mydb[colname]
        cursor = mycol.find()
        if colname == 'gainers':
            tab_headers = list(('Rank', 'Name'))            
            table_data = []
            for i,doc in enumerate(cursor): table_data.append([i+1,doc['security_name']])
            from tabulate import tabulate
            table = tabulate(table_data, headers=tab_headers, tablefmt='orgtbl')
            with open(constant.REPORT_BSE_FPATH, 'a') as f:
                f.write("COLLECTION: {}\n{}\n\n".format(colname, table))
        elif colname == 'loosers':
            tab_headers = list(('Rank', 'Name'))            
            table_data = []
            for i,doc in enumerate(cursor): table_data.append([i+1,doc['security_name']])
            from tabulate import tabulate
            table = tabulate(table_data, headers=tab_headers, tablefmt='orgtbl')
            with open(constant.REPORT_BSE_FPATH, 'a') as f:
                f.write("COLLECTION: {}\n{}\n\n".format(colname, table))
        elif colname == 'trending':
            tab_headers = [('Name')]            
            table_data = []
            keysset = set()
            for doc in cursor: table_data.append([doc['name']])
            from tabulate import tabulate
            table = tabulate(table_data, headers=tab_headers, tablefmt='orgtbl')
            with open(constant.REPORT_BSE_FPATH, 'a') as f:
                f.write("COLLECTION: {}\n{}\n\n".format(colname, table))

def main():
    gn = Generate()  
    with open(constant.REPORT_BSE_FPATH, 'w') as f:
        f.write("REPORT: BSE top 10 gainers, top 10 loosers and trending")
        f.write("\n[time stamp] {}\n\n".format(datetime.now().strftime("%B %d, %Y  %H:%M:%S")))        

    gn.all_coll_report(constant.BSE_DB)    

if __name__ == '__main__':
    main()



