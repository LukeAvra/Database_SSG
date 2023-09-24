# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 09:36:29 2023

@author: Luke Avra
"""

from configparser import ConfigParser
import os


absolute_path = os.path.join(os.path.dirname(__file__), "Database.ini")



###
#  filename points to the location of the Database.ini file, change when program is being run on a different machine
### C:/Users/Luke/Documents/Python Scripts/Database_SSG/Database - Python/
def config(filename=absolute_path, section='postgresql'):  
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        
    return db, params

def configDBVars(filename=absolute_path, section='database_table_names'):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        invDatabase = parser[section]['inventory_table']
        userDatabase = parser[section]['user_table']
        barDatabase = parser[section]['barcode_table']
        bomDatabase = parser[section]['bill_of_material_table']
        locDatabase = parser[section]['location_table']
        kitDatabase = parser[section]['kit_table']
        rmaDatabase = parser[section]['rma_table']

        return invDatabase, userDatabase, barDatabase, bomDatabase, locDatabase, kitDatabase, rmaDatabase


configDBVars()
