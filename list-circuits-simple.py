#!/bin/python
from stem import CircStatus
from stem.control import Controller


with Controller.from_port(port = 9051) as controller:
    controller.authenticate()

    for circ in sorted(controller.get_circuits()):
        if circ.status != CircStatus.BUILT:
            continue
    print("Circuit %s" % (circ.id))
