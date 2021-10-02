"""
Prints all times that availabilities will be checked 
"""

import datetime
import sys,os


#for local imports
# -----------------------------------
os.chdir('./src')
sys.path.append(os.getcwd())
# -----------------------------------
import mathHelper


start = datetime.datetime.now()
end = datetime.datetime.now() + datetime.timedelta(hours=.4)
interval = datetime.timedelta(minutes=15)

mathHelper.timesBetween(start, end, interval)