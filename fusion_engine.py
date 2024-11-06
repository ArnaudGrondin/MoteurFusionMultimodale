#!/usr/bin/env python

from ivy.std_api import *
IvyInit("fusion_engine")
IvyStart()
forme=""


def dollarN_callback(agent, arg):
    global forme
    forme = arg
    print("dollarN_callback: agent=%r arg=%r" % (agent, arg))
    

def sra5_callback(agent, arg):
    print("sra5_callback: agent=%r larg=%r" % (agent, arg))
    IvySendMsg("dollarN: "+forme)
    

IvyBindMsg(dollarN_callback, "^dollarN: (.*)")
IvyBindMsg(sra5_callback, "^sra5: (.*)")
IvyBindMsg(sra5_callback, ".*")