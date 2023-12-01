##!/bin/bash --login

# do we need to set envoronment here?

echo pf_restart_list.py $@
cd /home/n02/n02/mjmn02/PF/pf_puma

./pf_restart_list.py $@
