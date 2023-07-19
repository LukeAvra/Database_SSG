# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 09:36:29 2023

@author: Luke Avra
"""

from configparser import ConfigParser


###
#  filename points to the location of the Database.ini file, change when program is being run on a different machine
###
def config(filename='C:/Users/Luke/Documents/Python Scripts/Database_SSG/Database - Python/Database.ini', section='postgresql'):  
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        
    return db

def configDBVars(filename='C:/Users/Luke/Documents/Python Scripts/Database_SSG/Database - Python/Database.ini', section='database_table_names'):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        invDatabase = parser[section]['inventory_table']
        userDatabase = parser[section]['user_table']
        barDatabase = parser[section]['barcode_table']
        bomDatabase = parser[section]['bill_of_material_table']
        locDatabase = parser[section]['location_table']
        
        return invDatabase, userDatabase, barDatabase, bomDatabase, locDatabase



