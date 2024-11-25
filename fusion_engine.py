#!/usr/bin/env python
import ivy.std_api as ivyapi
from typing import Any

def info(fmt: str, *arg: Any) -> None:
    print(fmt % arg)

def on_connection_change(agent: ivyapi.IvyClient, event: int) -> None:
    if event == ivyapi.IvyApplicationDisconnected:
        info('Ivy application %r has disconnected', agent)
    else:
        info('Ivy application %r has connected', agent)
    apps = ivyapi.IvyGetApplicationList()
    info(
        'Ivy applications currently on the bus (count: %i): %s',
        len(apps),
        ','.join(apps),
    )


ivyapi.IvyInit("fusion_engine","hi",0,on_connection_change)
ivyapi.IvyStart()
forme=""





def dollarN_callback(agent, arg):
    global forme
    forme = arg
    print("dollarN_callback: agent=%r arg=%r" % (agent, arg))
    

def sra5_callback(agent, arg):
    print("sra5_callback: agent=%r larg=%r" % (agent, arg))
    ivyapi.IvySendMsg("dollarN: "+forme)
    

ivyapi.IvyBindMsg(dollarN_callback, "^dollarN: (.*)")
ivyapi.IvyBindMsg(sra5_callback, "^sra5: (.*)")
ivyapi.IvyBindMsg(sra5_callback, "(.*)")