import sys
import time
import os.path
import subprocess
import socket
from string import Template

if len(sys.argv) < 2 :
    print "Usage: python " + str(sys.argv[0]) + " <router_name>"
    sys.exit(1) 

options = {}
options["ROUTER_ADDRESS"] = socket.gethostbyname(socket.gethostname())
options["ROUTER_NICKNAME"] = sys.argv[1]

# Generate router keys
#cmd = ["sudo", "-u", "toranon", "tor", "--list-fingerprint", "--orport", "1", 
#"--dirserver", "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff",
#"--datadirectory", options["DATA_DIR"]]
#subprocess.check_call(cmd)


#
# Create torrc file
#
torrc_template = Template(" \
TestingTorNetwork 1 \n \
DataDirectory /var/lib/tor \n \
RunAsDaemon 1 \n \
ConnLimit 60 \n \
Nickname $ROUTER_NICKNAME \n \
ShutdownWaitLength 0 \n \
PidFile /var/lib/tor/pid \n \
Log notice file /var/lib/tor/notice.log \n \
Log info file /var/lib/tor/info.log \n \
ProtocolWarnings 1 \n \
SafeLogging 0 \n \
DisableDebuggerAttachment 0 \n \
DirAuthority RS4 orport=5000 no-v2 hs v3ident=8E9F5D42E1189A917490A3267EED0AE42AD3E8A6 40.117.38.173:7000 A237833CF716969614C5BF356C029ECFCB395590 \n\
SocksPort 9050 \n \
OrPort 5000 \n \
#Address 104.155.64.249 \n \
AssumeReachable 1 \n \
EnforceDistinctSubnets 0 \n \
UseEntryGuards 0 \n \
ControlPort 9051 \n \
CookieAuthentication 1 \n \
")

torrc_content = torrc_template.safe_substitute(options)

# Save the file contents
#if os.path.isfile(options["TORRC_PATH"]) :
#    subprocess.check_call(["mv", options["TORRC_PATH"], options["TORRC_PATH"]+"_backup_"+str(int(time.time()))]) 
f = open("/etc/tor/torrc", 'w')
f.write(torrc_content)
f.close()

