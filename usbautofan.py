# python3

# imports ----------------------------------------------------------------------------------------
import os
import re
import time
from datetime import datetime
from pathlib import Path

# define Variables -------------------------------------------------------------------------------
logfile = Path('log.txt')
maxtemp = 60	#degrees C (default = 60)
mintemp = 50	#degrees C (default = 50)
intervall = 60	#seconds

# define functions -------------------------------------------------------------------------------
def gettemp():
	cputempraw = os.popen('vcgencmd measure_temp').read()
	cputemp = re.search(r'[0-9]+.[0-9]+', cputempraw).group()
	return cputemp

def fancontrol(state):
	fancmd = 'uhubctl -l 1-1 -a '+str(state)+' > /dev/null'
	os.system(fancmd)
	#print(fancmd)

# action -----------------------------------------------------------------------------------------
while True:									# Just keeps running until aborted
	temp = gettemp()
	ttemp = int(float(temp))				# converts temp to mathable number (no decimals)
	if ttemp >= maxtemp:
		print(temp+'C	🥵	fan should be running')
		fancontrol(1)
	if ttemp <= mintemp:
		print(temp+"C	😎	fan should be off")
		fancontrol(0)
		print('	fan should be off\n')
	#print('waiting for '+str(intervall)+' seconds to recheck')
	time.sleep(intervall)