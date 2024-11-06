#!/usr/bin/env python

from ivy.std_api import *
from typing import Any

def info(fmt: str, *arg: Any) -> None:
    print(fmt % arg)

def on_connection_change(agent: IvyClient, event: int) -> None:
    if event == IvyApplicationDisconnected:
        info('Ivy application %r has disconnected', agent)
    else:
        info('Ivy application %r has connected', agent)
    apps = IvyGetApplicationList()
    info(
        'Ivy applications currently on the bus (count: %i): %s',
        len(apps),
        ','.join(apps),
    )


IvyInit("fusion_engine","hi",0,on_connection_change)
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
IvyBindMsg(sra5_callback, "(.*)")