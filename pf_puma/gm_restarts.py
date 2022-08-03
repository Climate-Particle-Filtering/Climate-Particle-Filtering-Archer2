#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2022
#
import copy
import os
import shutil
import argparse
import sys
import subprocess

from incrementRuntime import editRunLen
from gm_pf_accept_crunlist import get_requests

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Edit run end in a suite's conf file")
    parser.add_argument("dirpf",help="ensemble directory")
    parser.add_argument("increment_s", help="increment yr,mon,day,h,m,s")
    parser.add_argument("terminate_s", help="terminate yr,mon,day,h,m,s")

    parser.add_argument('--nDryrun','-n', default=False, action=argparse.BooleanOptionalAction, help="set to make no change to datasbase")
    parser.add_argument('--testing',
                        '-t',
                        required=False,
                        action='store_true',
                        help='set if running a test')
    parser.add_argument('--alldocs',
                        '-a',
                        required=False,
                        action='store_true',
                        help='see all docs for this PF directory')
    parser.add_argument('--projectName',
                        '-p',
                        required=False,
                        help='Name of the project (required if not in cfg file)')

    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")


    args = parser.parse_args()

      # note the ensemble directory is on Arcehr2, and used in the 
      # query to GeosMeta to select messages for an ensemble.
      # From GeosMeta get the list of suites that are ready for restart.

    crunlist = get_requests(args)
    print("number of requests in GeosMeta %d"%len(crunlist))
    print("crunlist")
    print(crunlist)
    if "(" in args.increment_s:
        incString=args.increment_s.split("(")[1].split(")")[0]
    if "(" in args.terminate_s:
        endString=args.terminate_s.split("(")[1].split(")")[0]
    if args.testing or args.nDryrun:
       print ("not restarting - test run")
    else:
        cmd = "rose suite-run --restart"
        for suitename in crunlist:
             suitedir=os.path.join(os.path.expanduser('~'),"roses",suitename)
             os.chdir(suitedir)
             canContinue = editRunLen(suitename, incString, endString)
             if canContinue:
                     rtn=subprocess.check_output(cmd, shell=True)
                     print ("gm_restarts: suite %s restarted\n"%suitename)
                     print (rtn)
             else:
                     print ("gm_restarts: suite %s reached its endtime"%suitename)








