#!/usr/bin/env python3
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= "Edit run end in a suite's conf file")
    parser.add_argument("increment_s", help="increment yr,mon,day,h,m,s")
    parser.add_argument("terminate_s", help="terminate yr,mon,day,h,m,s")
    parser.add_argument('crunlist',    help="comma separated list of suites")

    args = parser.parse_args()

      # note the ensemble directory is on Arcehr2, and used in the 
      # path to here must be set in .bashrc/.bash_profile

    crunlist = args.crunlist.split(',')
    print("pf_restart_list.py:  number of suites %d"%len(crunlist))
    print(crunlist)
    incString=args.increment_s
    endString=args.terminate_s
    if "(" in args.increment_s:
        incString=args.increment_s.split("(")[1].split(")")[0]
    if "(" in args.terminate_s:
        endString=args.terminate_s.split("(")[1].split(")")[0]
    print ("incString %s ; endString %s "%(incString, endString))
    for suitename in crunlist:
             suitedir=os.path.join(os.path.expanduser('~'),"roses",suitename)
             os.chdir(suitedir)
             canContinue = editRunLen(suitename, incString, endString)
             print ("returned canContinue %d\n"%canContinue)
             if canContinue:
                     cmd=("do_restart.sh %s"%(suitename))
                     rtn=subprocess.check_output(cmd, shell=True)
                     print ("suite %s restarted\n"%suitename)
                     print (rtn)
             else:
                     print ("suite %s reached its endtime"%suitename)








