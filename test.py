import os, sys, time
from multiprocessing import Process, Pool
from subprocess import *
import subprocess
from os import system

torcurl = "(time curl -s -o /dev/null --socks5-hostname 127.0.0.1:8666 WEBSITE) 3>&1 1>&2 2>&3 "
curl = "(time curl -s  -o /dev/null WEBSITE) 3>&1 1>&2 2>&3 "
reset = "(echo authenticate '\"\"'; echo signal newnym; echo quit) | nc localhost 8667"


webfile = open('./tor_bootstrap/websites', 'r')

def torrunner(website):
	commandz = torcurl.replace('WEBSITE', website)
	try:
		output = "TOR " + website + subprocess.Popen(commandz, shell=True, stdout=subprocess.PIPE).stdout.read()
		subprocess.Popen(reset, shell=True, stdout=subprocess.PIPE).stdout.read()
	except subprocess.CalledProcessError:
		return "FAILED " + website

def regrunner(website):
	commandz = curl.replace('WEBSITE', website)
	try:
		return "REGULAR " + website + subprocess.Popen(commandz, shell=True, stdout=subprocess.PIPE).stdout.read()
	except subprocess.CalledProcessError:
		return "FAILED " + website

sites = []
data = f.read()
lines = data.split('\n')
for line in lines:
	if line[0] == '#': continue
	sites.append(line.strip('\n'))



results = []
for site in sites:
	regrunner(site)

for i in range(0,10):
	results.append(regrunner(site))
	results.append(torrunner(site))
	
for result in results:
	print( result)

# pool_size = 4
# pool = Pool(processes=pool_size)
# resultsreg = pool.map(regrunner,sites)
# print resultsreg
# resultstor = pool.map(torrunner,sites)
# print resultstor

# print "RESULTS:"
# for result in resultsreg:
# 	print result
# for result in resultstor:
# 	print result
 










