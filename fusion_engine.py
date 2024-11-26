#!/usr/bin/env python
import ivy.std_api as ivyapi
from typing import Any


class FusionMotor:
    def __init__(self) -> None:
        ivyapi.IvyInit("fusion_engine", "hi", 0, self.on_connection_change)

        ivyapi.IvyStart()
        self.forme = ""
        self.sra5_string = ""
        self.sra5_token = []
        self.pos =(122,221)

    def info(self, fmt: str, *arg: Any) -> None:
        print(fmt % arg)

    def on_connection_change(self, agent: ivyapi.IvyClient, event: int) -> None:
        if event == ivyapi.IvyApplicationDisconnected:
            self.info("Ivy application %r has disconnected", agent)
        else:
            self.info("Ivy application %r has connected", agent)
        apps = ivyapi.IvyGetApplicationList()
        self.info(
            "Ivy applications currently on the bus (count: %i): %s",
            len(apps),
            ",".join(apps),
        )

    def dollarN_callback(self, agent, arg) -> str:
        self.forme = str(arg)
        print("dollarN_callback: agent=%r arg=%r" % (agent, arg))

    def sra5_callback(self, agent, arg):
        # print("sra5_callback: agent=%r arg=%r" % (agent, arg))
        ivyapi.IvySendMsg("dollarN: " + self.forme)
        self.sra5_processing(arg)

    def sra5_processing(self, sra5_string) -> str:
        self.sra5_token = sra5_string.split(" ")
        self.sra5_token[0] = self.sra5_token[0].replace("Parsed=", "")
        print(self.sra5_token)
    
    



if __name__ == "__main__":
    motor = FusionMotor()
    ivyapi.IvyBindMsg(motor.dollarN_callback, "^dollarN: (.*)")
    ivyapi.IvyBindMsg(motor.sra5_callback, "^sra5 (.*)")
    
    
    
    
    
    
    
    
    # ivyapi.IvyBindMsg(sra5_callback, "(.*)")
