#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
"""
exemplar of a filter function
inputs:
    runlist - input subdirectories
    currentcycle - Name of current cycle 
    topdir: their parent directoru
    restart_dir: name of directory to temporarily copy the restart files too.
    
output:
    list of tuples {runname, run used to overwirte its dump, dict of how that overwirte was done)
        eg. [(zd001, zd004, {perturbation: x_for_zd001}),
             (zd002. zd004, {perturbation: x_for zd002}),
             .... ]
             so here zd004 dumps were twice perturbed to continue the runs zd001 and 2.
"""
import os
def filter(runlist,currentcycle,topdir,restart_dir):
    # select runs whose dumps are to be used
    # for the run in the corresponding input runlist item
    # if there is anything to remember about how the dumps are perturbed,
    # put it int he corresponding list of dictionaries

    # this dummy function
    #    - let the filtering list just be an inverted list.
    #    - invent a list of dicts in case anythign to be remembered for each perturbation

    filteredlist=runlist[::-1]

    adictlist=[]

    for (i,item) in enumerate(filteredlist):
        val= 1000+i
        adictlist.append({'dummypar':val})

    #find every instance of restart files that are needed.
    restarts_used=[]
    for (i,item) in enumerate(filteredlist):
        if item not in restarts_used:
            restarts_used.append(item)
    print(restarts_used)
    #Make a copy of restart files needed
    for (i,item) in enumerate(restarts_used):
        print('mkdir -p '+restart_dir+item)
        os.system('mkdir -p '+restart_dir+item)
        print('mkdir -p '+restart_dir+item+'/CICEhist')
        os.system('mkdir -p '+restart_dir+item+'/CICEhist')
        print('mkdir -p '+restart_dir+item+'/NEMOhist')
        os.system('mkdir -p '+restart_dir+item+'/NEMOhist')
        #cp atmos dump
        print('cp '+topdir+item+'/share/data/History_Data/'+item+'a.da'+currentcycle+'_00 '+restart_dir+item+'/')
        os.system('cp '+topdir+item+'/share/data/History_Data/'+item+'a.da'+currentcycle+'_00 '+restart_dir+item+'/')
        #cp NEMO dump
        print('cp '+topdir+item+'/share/data/History_Data/NEMOhist/'+item+'o_*'+currentcycle+'_restart* '+restart_dir+item+'/NEMOhist/')
        os.system('cp '+topdir+item+'/share/data/History_Data/NEMOhist/'+item+'o_*'+currentcycle+'_restart* '+restart_dir+item+'/NEMOhist/')
        #cp CICE dump
        print('cp '+topdir+item+'/share/data/History_Data/CICEhist/'+item+'i.restart.'+currentcycle[:4]+'-'+currentcycle[4:6]+'-'+currentcycle[6:]+'-00000.nc '+restart_dir+item+'/CICEhist/')
        os.system('cp '+topdir+item+'/share/data/History_Data/CICEhist/'+item+'i.restart.'+currentcycle[:4]+'-'+currentcycle[4:6]+'-'+currentcycle[6:]+'-00000.nc '+restart_dir+item+'/CICEhist/')
    #For each simulation (particle) move the appropriate restart files back into the working model directory 
    for (i,WKens) in enumerate(runlist):
        RESTARTens=filteredlist[i]
        #cp perturbed atmos dump
        print('python $UMDIR/scripts/perturb_theta.py '+restart_dir+RESTARTens+'/'+RESTARTens+'a.da'+currentcycle+'_00 '+topdir+WKens+'/share/data/History_Data/'+WKens+'a.da'+currentcycle+'_00 ')
        os.system('python $UMDIR/scripts/perturb_theta.py '+restart_dir+RESTARTens+'/'+RESTARTens+'a.da'+currentcycle+'_00 '+topdir+WKens+'/share/data/History_Data/'+WKens+'a.da'+currentcycle+'_00 ')
        #cp NEMO dump
        for j, item in enumerate(os.listdir(restart_dir+RESTARTens+'/NEMOhist')):
             print('cp '+restart_dir+RESTARTens+'/NEMOhist/'+item+' '+topdir+WKens+'/share/data/History_Data/NEMOhist/'+item.replace(RESTARTens,WKens))
             os.system('cp '+restart_dir+RESTARTens+'/NEMOhist/'+item+' '+topdir+WKens+'/share/data/History_Data/NEMOhist/'+item.replace(RESTARTens,WKens))
        #cp CICE dump
        for j, item in enumerate(os.listdir(restart_dir+RESTARTens+'/CICEhist')):
             print('cp '+restart_dir+RESTARTens+'/CICEhist/'+item+' '+topdir+WKens+'/share/data/History_Data/CICEhist/'+item.replace(RESTARTens,WKens))
             os.system('cp '+restart_dir+RESTARTens+'/CICEhist/'+item+' '+topdir+WKens+'/share/data/History_Data/CICEhist/'+item.replace(RESTARTens,WKens))

    print('rm -rf '+restart_dir+'*')
    os.system('rm -rf '+restart_dir+'*')

    oittuples = list(zip(runlist, filteredlist,adictlist))


    # in real world for each tuple overwrite the necessary dump.
    # in this dummy case we assume that is done and just return the list of tuples
    # its used just to hold a record of what was done

    return oittuples;

tups=filter(['PN001','PN002'],'18500109','/work/n02/n02/schn02/cylc-run/','/work/n02/n02/shared/aschurer/PF/trail1/restart_files/')
print(tups)
                                                                                                                                                                                                 1,1           Top
