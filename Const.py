import getopt
import sys

# process arguments
(OPT, _) = getopt.getopt(sys.argv[1:], "du:p:", [
    "debug", "username", "password"])
OPT = dict(OPT)

DEBUG = '-d' in OPT or '--debug' in OPT
USERNAME = OPT['-u'] if OPT['-u'] != '' else OPT['--username']
PASSWORD = OPT['-p'] if OPT['-p'] != '' else OPT['--password']
CACHE_PATH = './data.json'
