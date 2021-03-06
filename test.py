import os, sys, time
from multiprocessing import Process, Pool
from subprocess import *
import subprocess
from os import system

torcurl = "(time curl -s -o /dev/null --socks5-hostname 127.0.0.1:8666 WEBSITE) 3>&1 1>&2 2>&3 "
curl = "(time curl -s  -o /dev/null WEBSITE ) 3>&1 1>&2 2>&3 "
reset = "(echo authenticate '\"\"'; echo signal newnym; echo quit) | nc localhost 8667"


webfile = open('./tor_bootstrap/websites', 'r')

def torrunner(website):
	commandz = torcurl.replace('WEBSITE', website)
	try:
		return "TOR " + website + subprocess.Popen(commandz, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
	except subprocess.CalledProcessError:
		return "FAILED " + website

def regrunner(website):
	commandz = curl.replace('WEBSITE', website)
	try:
		return "REGULAR " + website + subprocess.Popen(commandz, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
	except subprocess.CalledProcessError:
		return "FAILED " + website

data = webfile.read()
sites = data.split('\n')

results = []
for site in sites:
	regrunner(site)

for i in range(0,10):
	for site in sites:
		results.append(regrunner(site))
		results.append(torrunner(site))
	subprocess.Popen(reset, shell=True, stdout=subprocess.PIPE)

	
for result in results:
	print(result)