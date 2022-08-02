#!/bin/bash

# want python3 with some addon packages

export PATH=/work/n02/shared/mjmn02/sw/conda/opt_1/bin/:$PATH


   # following includes GeosMeta

echo $HOSTNAME  geosmeta setup archer2 
GMTOP=/work/n02/shared/mjmn02/geosmeta/GeosMetaClient_python/clientpy3

export PYTHONPATH=$PYTHONPATH:$GMTOP:$GMTOP/geosmeta
export PATH=$PATH:$GMTOP/bin

