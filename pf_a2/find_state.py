#!/usr/bin/env python3

from pathlib import Path
import argparse

# simple program that searches subdirectories in the input directory
# for the precence of a file called 'state'.args.state If the state file is present
# and contains the specified state (by default NEW) it will report the name
# of the subdirectory to standard out as a space separated list. 

def find_state(topdir, state='CRUN_READY'):
    runs = []
    fname= 'state.%s'%(state)
    if topdir is not None:
        for rd in topdir.iterdir():
           statefile = rd / fname
           if statefile.exists():
                runs.append(rd.name)
    return runs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('study', type=Path,
                        help='name of study directory')
    parser.add_argument('-s', '--state', #choices=STATES,
                        default='CRUN_READY',
                        help="look for run in particular state, default CRUN_READY")
    args = parser.parse_args()

    if not args.study.is_dir(): 
        parser.error('%s is not a directory'%(args.study))
    runs=find_state(args.study, args.state)
    if len(runs) > 0:
            print(' '.join(runs))

