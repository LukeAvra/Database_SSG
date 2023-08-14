# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 07:54:57 2023

@author: Luke

CommandLine Arguments:
    -l = local only
    -r = remote only
    -a = both
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from datetime import datetime
import time
import Database_Globals as DG

def insertion(sqlFile, database):
    cur = DG.conn.cursor()
    sql = '''SELECT * FROM ''' + database + ''';'''
    cur.execute(sql)
    records = cur.fetchall()
    for rec in records:
        if len(rec) > 1:
            sqlFile.write("INSERT INTO " + database + " VALUES " + str(rec) + ";\n")
        else:
            sqlFile.write("INSERT INTO " + database + " VALUES " + str(rec).replace(',', '') + ";\n")
    return


def main():
    DG.main()
    month = datetime.now().strftime("%B")
    year= datetime.now().strftime("%Y")
    dt_str = datetime.now().strftime("%B %d_%H-%M-%S")
    dbList = [DG.invDatabase, DG.locDatabase, DG.userDatabase, DG.bomDatabase, DG.barDatabase]
    
    def local():
        if(not os.path.exists(os.path.dirname(__file__) + "\\Database Backup\\" + year)):
            os.mkdir(os.path.dirname(__file__) + "\\Database Backup\\" + year)
        if(not os.path.exists(os.path.dirname(__file__) + "\\Database Backup\\" + year + "\\" + month)):
            os.mkdir(os.path.dirname(__file__) + "\\Database Backup\\" + year + "\\" + month)
            
        filePath = os.path.dirname(__file__) + "\\Database Backup\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
        sqlFile = open(filePath, 'w')
        
        for db in dbList:
            insertion(sqlFile, db)
            
        return 
    
    def share():
        shareBasePath = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra\\Database Backup"
        if(not os.path.exists(shareBasePath + "\\" + year)):
            os.mkdir(shareBasePath + "\\" + year)
        if(not os.path.exists(shareBasePath + "\\" + year + "\\" + month)):
            os.mkdir(shareBasePath + "\\" + year + "\\" + month)
        
        filePath = shareBasePath + "\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
        sqlFile = open(filePath, 'w')
        
        for db in dbList:
            insertion(sqlFile, db)        
        return
    
    def deleteOldFiles():
        folder = os.path.dirname(__file__) + "\\Database Backup\\"
        
        
        fileList = os.listdir()
        currentTime = time.time()
        
        # 'day' is the number of seconds in a day
        day = 86400
        minute = 60
        
        
        for (root, dirs, files) in os.walk(folder, topdown=True):
            for file in files:
                filePath = os.path.join(root, file)
                timestamp_of_file_modified = os.path.getmtime(filePath)
                lastModification = datetime.fromtimestamp(timestamp_of_file_modified)
                number_of_seconds = (datetime.now() - lastModification).seconds
                print(number_of_seconds)
        
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
