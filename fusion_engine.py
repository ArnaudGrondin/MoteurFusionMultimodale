#!/usr/bin/env python
import ivy.std_api as ivyapi
from typing import Any


class FusionMotor:
    def __init__(self) -> None:
        ivyapi.IvyInit("fusion_engine", "hi", 0, self.on_connection_change)
        ivyapi.IvyStart()
        ivyapi.IvyBindMsg(self.dollarN_callback, "^dollarN: (.*)")
        ivyapi.IvyBindMsg(self.sra5_callback, "^sra5 (.*)")
        self.forme = ""
        self.sra5_string = ""
        self.sra5_token: list = []
        self.pos = None
        self.state = "init"
        self.sra5_dict: dict = {}
        # self.state_machine("")
        
        
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

    def dollarN_callback(self, agent, arg) -> None:
        self.forme = str(arg)
        print("dollarN_callback: agent=%r arg=%r" % (agent, arg))
        if self.state == "pos":
            self.state = "dollarN"

    def sra5_callback(self, agent, arg):
        # print("sra5_callback: agent=%r arg=%r" % (agent, arg))
        self.sra5_processing(arg)

    def sra5_processing(self, sra5_string) -> None:
        self.sra5_token = sra5_string.split(" ")
        self.sra5_token[0] = self.sra5_token[0].replace("Parsed=", "")
        if len(self.sra5_token) > 3:
            self.sra5_dict = {item.split('=')[0]: item.split('=')[1] for item in self.sra5_token}
        print(self.sra5_dict)
        

    def state_machine(self, arg) -> None:
        while True:
            match self.state:
                case "init":
                    if self.pos is not None:
                        self.state = "pos"
                case "pos":
                    ivyapi.IvySendMsg("motor: " + self.sra5_string)
                case "dollarN":
                    pass
                    
        

if __name__ == "__main__":
    motor = FusionMotor()

    
    
    
    
    
    
    
    
    # ivyapi.IvyBindMsg(sra5_callback, "(.*)")
