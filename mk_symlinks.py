import sys
import json
import time
import os.path
import subprocess
from string import Template

if len(sys.argv) < 2 :
    print "Usage: python " + str(sys.argv[0]) + " <home_dir>"
    sys.exit(1) 

home_dir = sys.argv[1]
options = json.load(open("./config.json"))

subprocess.check_call(["ln", "-s", options["SYSTEM"]["DATA_DIR"] + "/notice.log", home_dir + "/notice.log"])
subprocess.check_call(["ln", "-s", options["SYSTEM"]["DATA_DIR"] + "/info.log", home_dir + "/info.log"])
subprocess.check_call(["ln", "-s", options["SYSTEM"]["TORRC_PATH"], home_dir + "/torrc"])

