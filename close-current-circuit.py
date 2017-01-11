#!/bin/python
# -*- coding: utf8 -*-
# -*- coding: cp850 -*
from stem import CircStatus
from stem.control import Controller
import geoip2.database

reader = geoip2.database.Reader('/root/docs/GeoLite2-City.mmdb')

with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    for circ in sorted(controller.get_circuits()):
        if circ.status != CircStatus.BUILT:
            continue

    print "Closing circuit "+circ.id+" :"
    print("")
    print("Circuit %s (%s)" % (circ.id, circ.purpose))
    for i, entry in enumerate(circ.path):
        div = '+' if (i == len(circ.path) - 1) else '|'
        fingerprint, nickname = entry

        desc = controller.get_network_status(fingerprint, None)
        address = desc.address if desc else 'unknown'
        response = reader.city(address)
        print div+', '+ fingerprint+', '+ nickname+', '+ address+', '+str(response.country.name)+', '+', '+str(response.location.latitude)+', '+ str(response.location.longitude)
    controller.close_circuit(circ.id)
#str(circ.id)
