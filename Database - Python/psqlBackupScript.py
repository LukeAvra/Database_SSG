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
import shutil
import Database_Globals as DG

def doubleCheck():
    DG.main()
    cur = DG.conn.cursor()
    dt_str = datetime.now().strftime("%B %d_%H-%M-%S")
    filePath = os.path.dirname(__file__) + "\\Database Backup\\BarTest" + dt_str + ".txt"
    barFile = open(filePath, 'w')
    
    sql = '''SELECT manufacturerid FROM ssg_inventory ORDER BY manufacturerid;'''
    cur.execute(sql)
    records = cur.fetchall()
    for record in records:
        barFile.write(record[0] + "\n")
    
    return

def accessBackup():
    basePath = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra\\Access Backup"
    dt_str = datetime.now().strftime("%B %d_%H-%M-%S")
    accessPath = basePath + "\\" + dt_str + ".accdb"
    shutil.copy2('//192.168.56.105/SSGMVCDatabase/MVC Database.accdb', accessPath)
    return

def insertion(sqlFile, database):
    cur = DG.conn.cursor()
    if(database == 'barcodes'):
        order = 'code'
    else:
        order = 'barcode'
    
    sql = '''SELECT * FROM ''' + database + ''' ORDER BY ''' + order + ''';'''
    cur.execute(sql)
    records = cur.fetchall()
    for rec in records:
        if len(rec) > 1:
            sqlFile.write("INSERT INTO " + database + " VALUES " + str(rec) + ";\n")
        else:
            sqlFile.write("INSERT INTO " + database + " VALUES " + str(rec).replace(',', '') + ";\n")
    return

def createFile(basePath):
    DG.main() 
    cur = DG.conn.cursor()
    month = datetime.now().strftime("%B")
    year= datetime.now().strftime("%Y")
    dt_str = datetime.now().strftime("%B %d_%H-%M-%S")
    dbList = [DG.invDatabase, DG.locDatabase, DG.barDatabase]
    
    if(not os.path.exists(basePath + "\\" + year)):
        os.mkdir(basePath + "\\" + year)
    if(not os.path.exists(basePath + "\\" + year + "\\" + month)):
        os.mkdir(basePath + "\\" + year + "\\" + month)
    
    filePath = basePath + "\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
    filePathForDump = basePath + "\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
    sqlFile = open(filePath, 'w')
    for db in dbList:
        insertion(sqlFile, db)
    

    buildsKitsAndRMAs = [DG.buildDatabase, DG.kitDatabase, DG.rmaDatabase]
    for db in buildsKitsAndRMAs:
        sql = '''SELECT name FROM ''' + db + ''';'''
        cur.execute(sql)
        names = cur.fetchall()
        for tableName in names:
            print(tableName[0])
            insertion(sqlFile, tableName[0])
        
    return

def share():
    basePath = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra\\Database Backup"
    try:
        createFile(basePath)
    except Exception as error:
        print("An error has occured: ", error)
    
    # Pulling this server down
    # Wasn't working prior to pulling down though, it wasn't showing up in the network folder
    # May have something to do with setting up a new usb with same name? Can't recall if I did that
# =============================================================================
# 
#     basePath = r"\\DESKTOP-NTLGQ4N\Avra\Backup"
#     try:
#         createFile(basePath)
#     except Exception as error:
#         print("An error has occured: ", error)
# =============================================================================

    return
    
def local():
    basePath = os.path.dirname(__file__) + "\\Database Backup"
    createFile(basePath)
    return

def deleteOldFiles(folder):
    for (root, dirs, files) in os.walk(folder, topdown=True):
        for file in files:
            filePath = os.path.join(root, file)
            timestamp_of_file_modified = os.path.getmtime(filePath)
            lastModification = datetime.fromtimestamp(timestamp_of_file_modified)
            number_of_seconds = (datetime.now() - lastModification).seconds
            number_of_days = (datetime.now() - lastModification).days
            if(number_of_days > 90):
                os.remove(filePath)
                print("Delete: ", file)
        for directory in dirs:
            dirPath = os.listdir(os.path.join(root, directory))
            if(len(dirPath) == 0):
                os.rmdir(os.path.join(root, directory))
                print("Delete Directory: ", os.path.join(root, directory))

def backupCall():
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
    accessBackup()
    return

def deletionCall():
    localFolder = os.path.dirname(__file__) + "\\Database Backup"
    remoteFolder = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra\\Database Backup"
    for i in range(2):
        deleteOldFiles(localFolder)
        deleteOldFiles(remoteFolder)
    return

def main(): 
    backupCall()
    deletionCall()
    #doubleCheck()
    return

if __name__ == "__main__":
    main()
