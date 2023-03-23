#!/usr/bin/env python3

from pathlib import Path
import argparse
import sys
import os
import json

# CODED IMPORT FOR THE FILTERING FUCNTION:

# the filter function that scans dumps and resets them is always called pf_filter.py
# Differnt ensemble will have a different instance, held in a different directory
# so the directory path is an inputi argument, but always holding pf_filter,py

PF_FILTER_MOD="pf_filter.py"
PF_ITERATION_FILE="pf_iteration.txt"

def find_state(topdir, state, newstate):
    runs = []
    fname= 'state.%s'%(state)
    if newstate is not None:
         newfname= 'state.%s'%(newstate)
    if topdir is not None:
        for rd in topdir.iterdir():
           statefile = rd / fname
           if statefile.exists():
               runs.append(rd.name)
           if newstate is not None:
               newstatefile=rd / newstate
               os.rename(statefile, newstatefile)

    runss=sorted(runs)
    print ("find_state returning %s" %runss)
    return runss

def reset_state(topdir, runs,  state, newstate):

    fname= 'state.%s'%(state)
    newfname= 'state.%s'%(newstate)

    for frun in runs:
                 # chcekc/recode next two!
       oldfile = "%s/%s/%s"%(topdir, frun, fname)
       newfile = "%s/%s/%s"%(topdir, frun, newfname)
       
       os.rename(oldfile, newfile)

def increment_iteration(pfdir):
    # file pfdir/interation.txt has the iteration number from 1
   f=open(PF_ITERATION_FILE,"r")
   current=int(f.read())
   f.close()

   nextit=current+1

   f=open(PF_ITERATION_FILE,"w")
   f.write('%d'% nextit)
   f.close()
   return (current,nextit)

def save_filtering_json(it_rec, last_it):
    jfile="filtered.%s"%last_it
    fj=open(jfile,"w")
    json.dump(it_rec,fj,indent=4)
    fj.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PFtopdir', type=Path,
                        help='name of top directory in which all interface dirs exist')
    parser.add_argument('filterFunctionDir', type=Path,
                        help='filepath to  python script with the pffilter.py function')
    args = parser.parse_args()

    if not args.PFtopdir.is_dir(): 
        parser.error('%s is not a directory'%(args.PFtopdir))
    pf_topdir=args.PFtopdir
    if not args.filterFunctionDir.is_dir(): 
        parser.error('%s is not a directory'%(args.filterFunctionDir))
    pf_filterdir=args.filterFunctionDir

    pf_filterdirS="%s"%(pf_filterdir)
    pf_fpath="%s/%s"%(pf_filterdir,PF_FILTER_MOD)
    if not os.path.isfile(pf_fpath):
        print ("expected file %s but not found"%pf_fpath)
        exit(1)

              # find the runs that need to be filtered

    runs=find_state(args.PFtopdir, "DONE", None)
    if len(runs) > 0:
            print(' '.join(runs))

             # for trace purposes check the iteration number
             # an increment it. (A set of runs is an iteration)

    (last_iteration, next_iteration)= increment_iteration(pf_topdir)
    print("ending iteration %s starting %s"%(last_iteration, next_iteration))

               # IMPORT OF FILTER FUNCTION FROM PATH GIVEN BY USER
               
               # find the filter function PF_FILTER_MOD
               # any nested imports called by  it  need to be in the filepath....

    sys.path[0:0]=[pf_filterdirS]

#    print(sys.path)
    
    from  pf_filter import filter

               # run it - the returned list of tuples defines the lis tof runs to be contuinued
               # so filtering could - if needed - drop a run at this point.

    run_filter_dict_list = filter(runs, pf_topdir)

   
    print (" after filter %s" %run_filter_dict_list)

            # save what was done in a json file
            # with a etter definition of hte return data, this can be unnecessary.

    it_record=[]
    it_runs=[]

    for (run,dump,pert) in run_filter_dict_list:
       it_record.append([run, dump, pert])
       it_runs.append(run)

    reset_state(pf_topdir, it_runs, "DONE", "CRUN_READY")
        
    save_filtering_json(it_record, last_iteration)

            # option  uncoded save it also in geosmeta

#    save_filtering_geosmeta(it_record, last_iteration)
           


