# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:59:41 2023

@author: Luke

Client Script
"""

import os
import tqdm
import socket

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

# All of this should be set in a .ini file
host = "192.168.56.54"
port = 30001
filename = "test.txt"
# This will need to incorporate a full path to the filename, 
# maybe use 'os.path.dirname(__file__) + "\\" + filename' if in current directory
# os.path.join(os.path.dirname(__file__), filename) should work as well
filesize = os.path.getsize(filename)
