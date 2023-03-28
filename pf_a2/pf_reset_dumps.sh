#!/bin/bash

echo ensemble directory $1 
PFDIR=$1
cd $PFDIR

# identify the suites whose dumps need reworking
# their runs have file "state.DONE"

suitelist=""
for sdirf in $(find . -name "state.DONE")
do
    echo $sdirf
    suitelist=$(echo $suitelist $(dirname $sdirf))
done

# now have a space separated list, can be passed to python, or put above 
# logic into a python script

# here do the work to reset the dump files

echo "working on suites in directories" $suitelist

# next bit is dummy - want a file state.CRUN_READY in each suit directory where
# a restart is needed.
# Does allow some runs to be dropped, if the filtering returns a different list.

for sdirf in $suitelist
do
    echo mv  $sdirf/"state.DONE" $sdirf/"state.CRUN_READY"
    mv  $sdirf/"state.DONE" $sdirf/"state.CRUN_READY"
done




