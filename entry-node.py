from stem import CircStatus
from stem.control import Controller
import geoip2.database
reader = geoip2.database.Reader('/root/docs/GeoLite2-City.mmdb')



with Controller.from_port() as controller:
    controller.authenticate()

    for circ in controller.get_circuits():
        if circ.status != CircStatus.BUILT:
            continue  # skip circuits that aren't yet usable

        entry_fingerprint = circ.path[0][0]
        entry_descriptor = controller.get_network_status(entry_fingerprint, None)
        addr=entry_descriptor.address
        response = reader.city(addr)
        if entry_descriptor:
            print "Circuit %s : %s , %s , %s , %s " % (circ.id, addr, str(response.country.name),str(response.location.latitude), str(response.location.longitude)     )
        else:
            print "Unable to determine the address belonging to circuit %s" % circ.id
