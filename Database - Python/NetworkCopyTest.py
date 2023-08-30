# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 07:41:05 2023

@author: Luke
"""
import subprocess
import shutil
import os

# =============================================================================
# networkPath = '\\192.168.56.240\Avra\Backup'
# winCMD = 'net use ' + networkPath + ' /user:Admin SSGllc2023@)@#'
# subprocess.Popen(winCMD, stdout=subprocess.PIPE, shell=True)
# 
# =============================================================================
# =============================================================================
# shutil.copy2('C:\\Users\\Luke\\Documents\\Python Scripts\\Database_SSG\\Database - Python\\Database.ini', r"\\DESKTOP-NTLGQ4N\Avra\Database.ini")
# =============================================================================


basePath = r"\\DESKTOP-NTLGQ4N\Avra"
os.mkdir(basePath + "\\" + "Booty")