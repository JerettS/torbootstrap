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
# DisableDebuggerAttachment 0 \n\
DirServer PLDIR orport=5000 no-v2 hs v3ident=D1F6F2BD96C7A582D52404394D846F28E1746E2E 192.168.1.4:7000 D2DD4ADA3BB34D8187EA4CFC1121038C7E63DFE5\n\
\n\
SocksPort 8666\n\
OrPort 5000\n\
Address $ROUTER_ADDRESS\n\
AssumeReachable 1\n\
EnforceDistinctSubnets 0\n\
UseEntryGuards 0\n\
ControlPort 8667\n\
CookieAuthentication 1\n\
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
#if os.path.isfile(options["TORRC_PATH"]) :
#    subprocess.check_call(["mv", options["TORRC_PATH"], options["TORRC_PATH"]+"_backup_"+str(int(time.time()))]) 
f = open("/etc/tor/torrc", 'w')
f.write(torrc_content)
f.close()

