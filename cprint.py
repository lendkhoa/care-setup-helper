import errno
import os
import platform
import re
import sys
import subprocess
from itertools import islice

"""
Customize printer

Author: Khoa Le
Version: Nov 19, 2021
"""

class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

def cprint(message, color):
    version = sys.version[0:1]
    if int(version) > 2:
        print("{0}{1}{2}".format(color,message,bcolors.ENDC))
    else:
        message = u' '.join((message, "")).encode('utf-8').strip()
        print("{0}{1}{2}".format(color,message,bcolors.ENDC))
