#!/usr/bin/env python
#
# Copyright (c) The University of Edinburgh, 2014.
#
"""
exemplar of a filter function
inputs:
    runlist - input subdirectories
    topdir: their parent directoru
output:
    list of tuples {runname, run used to overwirte its dump, dict of how that overwirte was done)
        eg. [(zd001, zd004, {perturbation: x_for_zd001}),
             (zd002. zd004, {perturbation: x_for zd002}),
             .... ]
             so here zd004 dumps were twice perturbed to continue the runs zd001 and 2.
"""
def filter(runlist,topdir):
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

    oittuples = list(zip(runlist, filteredlist,adictlist))


    # in real world for each tuple overwrite the necessary dump.
    # in this dummy case we assume that is done and just return the list of tuples
    # its used just to hold a record of what was done

    return oittuples;
