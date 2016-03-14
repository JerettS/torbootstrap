import os, sys, time
from multiprocessing import Process, Pool
from subprocess import *
import subprocess

torcurl = ["time curl --socks5-hostname 127.0.0.1:8666 WEBSITE"]
curl = ["time curl WEBSITE"]
reset = ["(echo authenticate '\"\"'; echo signal newnym; echo quit) | nc localhost 8667"]


webfile = open('.tor_bootstrap/websites', 'r')

#			 sudo -S chmod -R 777 ./tor_bootstrap ;\
#			sudo -S chown -R toranon /etc/tor ; \

#			 sudo -S -u toranon echo \"blahblahbah\" | sudo -S /etc/tor/torrc ;\


def torrunner(website):
	commandz = map(lambda x: x.replace('WEBSITE', website), torcurl)
	try:
		output =  website + subprocess.check_output(commandz)
		subprocess.check_output(reset)
	except subprocess.CalledProcessError, e:
		return "FAILED " + website

def regrunner(website):
	commandz = map(lambda x: x.replace('WEBSITE', website), curl)
	try:
		return website + subprocess.check_output(commandz)
	except subprocess.CalledProcessError, e:
		return "FAILED " + website

sites = []
for line in webfile:
	if line[0] == '#': continue
	sites.append((line.strip('\n'), torcurl))

pool_size = 4
pool = Pool(processes=pool_size)
resultsreg = pool.map(regrunner,nodes)
print resultsreg
resultstor = pool.map(torrunner,nodes)
print resultstor

print "RESULTS:"
for result in resultsreg:
	print result
for result in resultstor:
	print result
 










