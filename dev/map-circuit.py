#!/bin/python
# -*- coding: utf8 -*-
# -*- coding: cp850 -*
from stem import CircStatus
from stem.control import Controller
import geoip2.database
from shutil import copyfile
import os
from time import gmtime, strftime
import shutil
import io
import webbrowser
import numpy as np

# LOCAL FILES

map_template="map/map-template.html"
directory_for_maps='circuits'

reader = geoip2.database.Reader('map/GeoLite2-City.mmdb')

circuit_lat=[]
circuit_lon=[]

# LOCAL COORDINATES

from json import load
from urllib2 import urlopen
import geoip2.database
reader = geoip2.database.Reader('map/GeoLite2-City.mmdb')

address =  load(urlopen('http://jsonip.com'))['ip']
response = reader.city(address)

local_lat=str(response.location.latitude)
local_lon=str(response.location.longitude)


with Controller.from_port(port = 9051) as controller:
    controller.authenticate()

    for circ in sorted(controller.get_circuits()):
        if circ.status != CircStatus.BUILT:
            continue

    print("Circuit %s (%s)" % (circ.id, circ.purpose))
    circuit_directory=directory_for_maps+"/circuit_"+circ.id+"_"+strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    os.makedirs(circuit_directory)

    map_circuit=circuit_directory+"/circuit.html"
    map_nodes = [circuit_directory+"/node0.html",circuit_directory+"/node1.html",circuit_directory+"/node2.html",circuit_directory+"/node3.html"]

    # PLOT GENERAL CIRCUIT

    with open(map_template, "r") as inp, open(map_circuit, "w") as output:
        for line in inp:
            l = line.strip()
            if l.endswith("locations = ["):
                output.write(format(l))
                # Add local coordinates
                string='\n[\''+response.country.name+'\', '+local_lat+', '+local_lon+', 1 ] ,'
                output.write(string)
                for i, entry in enumerate(circ.path):
                    div = '+' if (i == len(circ.path) - 1) else '|'
                    fingerprint, nickname = entry
                    desc = controller.get_network_status(fingerprint, None)
                    address = desc.address if desc else 'unknown'
                    response = reader.city(address)
                    desc = controller.get_network_status(fingerprint, None)
                    address = desc.address if desc else 'unknown'
                    response = reader.city(address)
                    string='\n[\''+response.country.name+'\', '+str(response.location.latitude)+', '+str(response.location.longitude)+', 1 ] ,\n'
                    output.write(string)
                    circuit_lat.append(response.location.latitude)
                    circuit_lon.append(response.location.longitude)
            elif l.startswith("zoom:"):
                string="zoom: 7 , \n"
                output.write(string)
            elif l.startswith("center:"):
                output.write("{}\n".format(l))
                string="center: new google.maps.LatLng("+str(np.mean(circuit_lat))+","+str(np.mean(circuit_lon))+") , \n"
                output.write(string)
            elif l.startswith("title:"):
                    string="\ntitle: \"circ_"+str(circ.id)+"_"+strftime("%Y-%m-%d_%H-%M-%S", gmtime())
                    output.write(string)
            else:
                output.write("{}\n".format(l))

webbrowser.open(map_circuit)

# MAP OF EACH NODE NEIGHBORHOOD

with Controller.from_port(port = 9051) as controller:
    controller.authenticate()

    for circ in sorted(controller.get_circuits()):
        if circ.status != CircStatus.BUILT:
            continue
        node_num=0
    for i, entry in enumerate(circ.path):
        div = '+' if (i == len(circ.path) - 1) else '|'
        fingerprint, nickname = entry

        desc = controller.get_network_status(fingerprint, None)
        address = desc.address if desc else 'unknown'
        response = reader.city(address)
        print div+', '+ fingerprint+', '+ nickname+', '+ address+', '+str(response.country.name)+', '+', ( '+str(response.location.latitude)+', '+ str(response.location.longitude)+' )'
        with open(map_template , "r") as inp, open(map_nodes[node_num], "w") as output:
            for line in inp:
                l = line.strip()
                if l.endswith("locations = ["):
                    output.write("{}\n".format(l))
                    string='\n[\''+response.country.name+'\', '+str(response.location.latitude)+', '+str(response.location.longitude)+', 1 ] ,\n'
                    output.write(string)
                elif l.startswith("center:"):
                    string="center: new google.maps.LatLng("+str(response.location.latitude)+', '+str(response.location.longitude)+") , \n"
                    output.write(string)
                elif l.startswith("zoom:"):
                    string="zoom: 15 , \n"
                    output.write(string)
                elif l.startswith("title:"):
                    string="\ntitle: \"circ_"+str(circ.id)+"_"+node+"_"+node_num+"_"+strftime("%Y-%m-%d_%H-%M-%S", gmtime())
                    output.write("{}\n".format(l))
                else:
                    output.write("{}\n".format(l))
        node_num+=1




for i in range(0,3):
    webbrowser.open(map_nodes[i])
#print response.city
