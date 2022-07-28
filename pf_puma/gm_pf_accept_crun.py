#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
from geosmeta import GeosMETA
from geosmeta import util
import argparse
import json
import sys
import os
import subprocess

def get_requests(args):

    projectName = args.projectName
    dirpf = args.dirpf
    if args.alldocs:
       query = '"gmdata.pfdir":"%s"'%dirpf

    elif args.testing: 
      query = '"gmdata.pf_rose_type":"crunTest","gmdata.pf_status":"NEW","gmdata.pfdir":"%s"'%dirpf
    else:
      query = '"gmdata.pf_rose_type":"crunRequest","gmdata.pf_status":"NEW","gmdata.pfdir":"%s"'%dirpf
   
    gm = GeosMETA(configFilePath=args.config_file)
 
    resultJSON = gm.findActivities("A",projectName, query, None)

    if args.testing or args.alldocs:
           print((json.dumps(resultJSON,
                                indent=2,
                                sort_keys=True)))

    #print("\n no. docs: %d\n"%(len(resultJSON['_items'])))

     # to do maybe should return tuples, if we think of pumatest as a server of model clones.
     # need a quick test for now!
    runlist = []
    if not args.alldocs:
        for itm in resultJSON['_items']:
            #print(itm['_id'])
            runlist.append(  itm['gmdata']['runname'] )
            activityEtag = itm['_etag']
            result = gm.updateActivity(itm['_id'],activityEtag,"gmdata.pf_status", "CONTINUING")
    return (runlist)

if __name__ == '__main__':
        # Get command line arguments
    parser = argparse.ArgumentParser(description="Find gmDocs given a user's query")
    parser.add_argument('--projectName',
                        '-p',
                        required=False,
                        help='Name of the project (required if not in cfg file)')

    parser.add_argument('--config-file','-C',metavar='FILE',help="read configuration from FILE: default:~/.geosmeta/geosmeta.cfg")

    parser.add_argument('--nDryrun','-n', default=False, action=argparse.BooleanOptionalAction, help="set to make no change to datasbase")

    parser.add_argument('--dirpf',
                        '-d',
                        required=True,
                        default=None,
                        help='ensemble directory for the PF')

    parser.add_argument('--alldocs',
                        '-a',
                        required=False,
                        action='store_true',
                        help='see all docs for this PF directory')
    parser.add_argument('--testing',
                        '-t',
                        required=False,
                        action='store_true',
                        help='set if running a test')

    args = parser.parse_args()

    runlist = get_requests(args)

    myscript="/home/mjm/dev/ModelOptimisation/Rose/onPUMA/continueRun.sh "
    for req_run in runlist:
    
        cmd = "%s %s"%(myscript, req_run)
        if args.nDryrun or args.testing or args.alldocs:
              print ("dryrun for %s"%cmd)
        else:
           print("running: %s\n"%cmd)
           rtn=subprocess.check_output(cmd, shell=True)
           print (rtn)

    if len(runlist)==0:
       print ("no runs to continue")
    

