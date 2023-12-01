#!/bin/bash --login

set -x
echo in puma2_restart.sh $@
echo nargs $#

cd /home/n02/n02/mjmn02/PF/pf_puma

echo hardcoded cd

runidl=${@##* }
runid=${runidl##* }
echo runid $runid

./puma2_restart.py "$@"
if [[ $? == "0"  ]]
then
    cd ~/roses/$runid
    rose suite-run --restart
else
	echo no restart wanted
fi

