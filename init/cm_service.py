#!/opt/anaconda/bin/python
import sys, os 
from optparse import OptionParser
import subprocess
import time
from cm_api.api_client import ApiResource

def main():
    s,a = arg_handle()
    for i in range(0,15):
        while True:
            try:
                cm_host = "127.0.0.1"
                api = ApiResource(cm_host, username="admin", password="admin")
                cdh=api.get_all_clusters()[0]
            except:
                print "Failed to connect to Cloudera Manager."
                print "Attempting to connect to Cloudera Manager..."
                time.sleep(15)
                continue
            break
    srv=cdh.get_service(s)
    actions[a](srv,s)

def srv_start(srv,s):
    print "Starting " + s + "..."
    cmd = srv.restart().wait()
    print s + " Start: " + ("Success" if cmd.success else "Fail")

def srv_restart(srv,s):
    print "Restarting " + s + "..."
    cmd = srv.restart().wait()
    print s + " Restart: " + ("Success" if cmd.success else "Fail")

def srv_stop(srv,s):
    print "Stoping " + s + "..."
    cmd = srv.restart().wait()
    print s + " Stop: " + ("Success" if cmd.success else "Fail")

def arg_handle():
    usage = "usage: cm_service.py <service> <action>"
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Wrong Number of Arguments")
    s = args[0]
    a = args[1]
    return s,a

if __name__ == "__main__":
    actions = {'start'   : srv_start,
               'restart' : srv_restart,
               'stop'    : srv_stop}
    main()





