import sys
import json
import time
import os.path
import subprocess
from string import Template

if len(sys.argv) < 3 :
    print "Usage: python " + str(sys.argv[0]) + " <router_address> <router_name>"
    sys.exit(1) 

options = json.load(open("./config.json"))
options["ROUTER_ADDRESS"] = sys.argv[1]
options["ROUTER_NICKNAME"] = sys.argv[2]

# Generate router keys
cmd = ["sudo", "-u", "debian-tor", "tor", "--list-fingerprint", "--orport", "1", 
"--dirserver", "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff",
"--datadirectory", options["SYSTEM"]["DATA_DIR"]]
subprocess.check_call(cmd)


#
# Create torrc file
#
torrc_template = Template("\
TestingTorNetwork 1 \n\
DataDirectory /var/lib/tor \n\
RunAsDaemon 1 \n\
ConnLimit 60 \n\
Nickname $ROUTER_NICKNAME \n\
ShutdownWaitLength 0 \n\
PidFile /var/lib/tor/pid \n\
Log notice file /var/lib/tor/notice.log \n\
Log info file /var/lib/tor/info.log \n\
ProtocolWarnings 1 \n\
SafeLogging 0 \n\
DisableDebuggerAttachment 0 \n\
DirAuthority $DIR_NICKNAME orport=$OR_PORT no-v2 hs v3ident=$DIR_AUTH_CERTIFICATE $DIR_ADDRESS:$DIR_PORT $DIR_FINGERPRINT\n\
\n\
SocksPort $SOCKS_PORT\n\
OrPort $OR_PORT\n\
Address $ROUTER_ADDRESS\n\
\n\
# An exit policy that allows exiting to IPv4 LAN\n\
# ExitPolicy accept 192.168.1.0/24:*\n\
\n\
# An exit policy that allows exiting to IPv6 localhost\n\
# ExitPolicy accept [::1]:*\n\
# IPv6Exit 1\n\
")

torrc_content = torrc_template.safe_substitute(options)

# Save the file contents
if os.path.isfile(options["SYSTEM"]["TORRC_PATH"]) :
    subprocess.check_call(["mv", options["SYSTEM"]["TORRC_PATH"], options["SYSTEM"]["TORRC_PATH"]+"_backup_"+str(int(time.time()))]) 
f = open(options["SYSTEM"]["TORRC_PATH"], 'w')
f.write(torrc_content)
f.close()

