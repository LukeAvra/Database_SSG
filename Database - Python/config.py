# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 09:36:29 2023

@author: Luke Avra
"""

from configparser import ConfigParser


# =============================================================================
# def config(filename='database.ini', section='postgresql'):
# =============================================================================
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




