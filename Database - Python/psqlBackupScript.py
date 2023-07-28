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


#os.chdir('C:\\Program Files\\PostgreSQL')
# =============================================================================
# os.system('''set "PGPASSWORD=SSGllc2023@)@#" && psql -U postgres -d backtest -c "SELECT * FROM test" && set "PGPASSWORD=""''')
# =============================================================================
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

    # CREATE DIRECTORY PER DAY, DIRECTORY SHOULD 5 FILES, ONE FOR EACH DATABASE
    #filePath = os.path.dirname(__file__) + "\\test.sql"    
    month = datetime.now().strftime("%B")
    day = datetime.now().strftime("%d")
    year= datetime.now().strftime("%Y")
    
    # Local check for year/month directories
    if(not os.path.exists(os.path.dirname(__file__) + "\\" + year)):
        os.mkdir(os.path.dirname(__file__) + "\\" + year)
    if(not os.path.exists(os.path.dirname(__file__) + "\\" + year + "\\" + month)):
        os.mkdir(os.path.dirname(__file__) + "\\" + year + "\\" + month)
    
    # Sharepoint check for year/month directories
    shareBasePath = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra"
    if(not os.path.exists(shareBasePath + "\\" + year)):
        os.mkdir(shareBasePath + "\\" + year)
    if(not os.path.exists(shareBasePath + "\\" + year + "\\" + month)):
        os.mkdir(shareBasePath + "\\" + year + "\\" + month)
        
    dt_str = datetime.now().strftime("%B %d_%H-%M-%S")
    
    # Filepath and writing file for local machine
    filePath = os.path.dirname(__file__) + "\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
    sqlFile = open(filePath, 'w')
    
    # Filepath and writing file for Sharepoint file
    filePath = shareBasePath + "\\" + year + "\\" + month + "\\" + dt_str + ".sql" 
    sqlFile = open(filePath, 'w')
    
    #os.mkdir("C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra"  + "\\" + year + "\\" + month)
    
# =============================================================================
#     
#     os.mkdir(os.path.dirname(__file__) + "\\" + dt_str)
#     filePath = os.path.dirname(__file__) + "\\" + dt_str + "\\database.sql"
#     sqlFile = open(filePath, 'w')    
# =============================================================================

    insertion(sqlFile, DG.invDatabase)
    insertion(sqlFile, DG.locDatabase)
    insertion(sqlFile, DG.userDatabase)
    insertion(sqlFile, DG.bomDatabase)
    insertion(sqlFile, DG.barDatabase)

    
    
    return

if __name__ == "__main__":
    main()
