# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 07:54:57 2023

@author: Luke
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from datetime import datetime
import Database_Globals as DG

def insertion(sqlFile, database):
    cur = DG.conn.cursor()
    sql = '''SELECT * FROM ''' + database + ''';'''
    cur.execute(sql)
    records = cur.fetchall()
    for rec in records:
        sqlFile.write("INSERT INTO " + database + " VALUES (" + str(rec) + ");\n")
        
    return


def main():
    DG.main()
    month = datetime.now().strftime("%B")
    year= datetime.now().strftime("%Y")
    dt_str = datetime.now().strftime("%B %d_%H-%M-%S")
    dbList = [DG.invDatabase, DG.locDatabase, DG.userDatabase, DG.bomDatabase, DG.barDatabase]
    
    def local():
        if(not os.path.exists(os.path.dirname(__file__) + "\\" + year)):
            os.mkdir(os.path.dirname(__file__) + "\\" + year)
        if(not os.path.exists(os.path.dirname(__file__) + "\\" + year + "\\" + month)):
            os.mkdir(os.path.dirname(__file__) + "\\" + year + "\\" + month)
            
        filePath = os.path.dirname(__file__) + "\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
        sqlFile = open(filePath, 'w')
        
        for db in dbList:
            insertion(sqlFile, db)
            
        return 
    
    def share():
        shareBasePath = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra"
        if(not os.path.exists(shareBasePath + "\\" + year)):
            os.mkdir(shareBasePath + "\\" + year)
        if(not os.path.exists(shareBasePath + "\\" + year + "\\" + month)):
            os.mkdir(shareBasePath + "\\" + year + "\\" + month)
        
        filePath = shareBasePath + "\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
        sqlFile = open(filePath, 'w')
        
        for db in dbList:
            insertion(sqlFile, db)        
        return
    
    numArg = len(sys.argv)
    if(numArg > 2):
        print("Too many commandline arguments")
        return
    if(numArg > 1):
        if(sys.argv[1] == '-l'):
            local()
        if(sys.argv[1] == '-r'):
            share()
        if(sys.argv[1] == '-a'):
            local()
            share()
    else:
        local()
        share()

    return

if __name__ == "__main__":
    main()
