# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 12:26:59 2023

@author: Luke
"""
import time
from datetime import datetime
import os

def deleteOldFiles(folder):
     
# =============================================================================
#     day = 86400
#     minute = 60
#     month = day * 31
# =============================================================================
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
#                dirs_to_delete.append(os.path.join(root, directory))
                os.rmdir(os.path.join(root, directory))
                print("Delete Directory: ", os.path.join(root, directory))
        
# =============================================================================
#     for i in dirs_to_delete:
#         os.remove(i)
#         print("Delete: ", i)
# =============================================================================

def main():
    localFolder = os.path.dirname(__file__) + "\\Database Backup"
    remoteFolder = "C:\\Users\\Luke\\Special Services Group, LLC\\SSG Customer Access - Documents\\Avra\\Database Backup"
    for i in range(2):
        deleteOldFiles(localFolder)
        deleteOldFiles(remoteFolder)
    return

if __name__ == "__main__":
    main()