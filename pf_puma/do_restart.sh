#!/bin/bash --login

echo in do_restart.sh $@
cd ~/roses/$1
echo $PWD rose suite-run --restart --no-gcontrol
rose suite-run --restart --no-gcontrol
echo "status after rose restart "$?

