#!/usr/bin/env python
# Elio Genson - nov/dec 2024
import ivy.std_api as ivyapi
from typing import Any
import time
from copy import deepcopy
import signal
import sys

class FusionMotor:
    def __init__(self) -> None:
        ivyapi.IvyInit("fusion_engine", "hi", 0, self.on_connection_change)
        ivyapi.IvyStart()
        ivyapi.IvyBindMsg(self.dollarN_callback, "^dollarN: (.*)")
        ivyapi.IvyBindMsg(self.sra5_callback, "^sra5 (.*)")
        ivyapi.IvyBindMsg(self.pos_callback, "^pos: (.*)")
        ivyapi.IvyBindMsg(self.mouse_callback,"^mouse (.*) ")
        self.forme: str = ""
        self.sra5_string: str = ""
        self.sra5_token: list = []
        self.bool_print = True
        self.pos = None
        self.state = "init"
        self.sra5_dict: dict = {
            "action": "undifined",
            "where": "undefined",
            "form": "undefined",
            "color": "undefined",
            "localisation": "undefined",
            "Confidence": "undefined",
            "NP": "undefined",
            "Num_A": "undefined",
        }
        self.output_dict: dict = deepcopy(self.sra5_dict)
        
        self.running = True
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
        self.output_dict["form"] = self.forme
        if self.state == "pos":
            self.state = "dollarN"
        self.bool_print = True

    def pos_callback(self, agent, arg) -> None:
        self.pos = str(arg)
        print("pos_callback: agent=%r arg=%r" % (agent, arg))
        if self.state == "init":
            self.state = "pos"
        self.bool_print = True

    def sra5_callback(self, agent, arg)-> None:
        # print("sra5_callback: agent=%r arg=%r" % (agent, arg))
        self.sra5_processing(arg)
        if self.state =="pos" and len(self.sra5_dict) > 3:
            self.state = "sra5"
        elif self.state == "dollarN":
            self.state = "color"
        self.bool_print = True
    def mouse_callback(self,agen,arg)-> None:
        print("mouse_callback: agent=%r arg=%r" % (agent, arg))
        self.pos = int(arg)
        self.state = "pos"
        self.bool_print = True
        pass

    def sra5_processing(self, sra5_string) -> None:
        self.sra5_token = sra5_string.split(" ")
        self.sra5_token[0] = self.sra5_token[0].replace("Parsed=", "")
        if len(self.sra5_token) > 3:
            self.sra5_dict = {item.split('=')[0]: item.split('=')[1] for item in self.sra5_token}
        self.bool_print = True
        




    def state_machine(self, arg=None) -> None:
        match self.state:
            case "init":
                time.sleep(0.2)
                if self.bool_print:
                    print("cliquez sur processing a la position ou vous voulez votre forme")
                    self.bool_print = False
            case "pos":
                time.sleep(0.2)
                if self.bool_print:
                    print("déssiner une forme sur le DollarN ou énoncer le dessin")
                    self.bool_print = False
            case "dollarN":
                time.sleep(0.2)
                if self.bool_print:
                    print("énoncez la couleur de la forme")
                    self.bool_print = False
            case "color":
                self.output_dict["color"] = self.sra5_dict["color"]
                time.sleep(0.2)
                self.state = "end"
            case "sra5":
                self.output_dict = deepcopy(self.sra5_dict)
                time.sleep(0.2)
                self.state = "end"
            case "end":
                ivyapi.IvySendMsg("fusion_engine: " + str(self.output_dict))
                self.state = "init"
            case _:
                time.sleep(0.2)
                
        

    def signal_handler(self, sig, frame):
        print('You pressed Ctrl+C!')
        self.running = False
        sys.exit(0)

if __name__ == "__main__":
    motor = FusionMotor()

    signal.signal(signal.SIGINT, motor.signal_handler)
    
    while motor.running:
        motor.state_machine()
    
    
    
    
    

