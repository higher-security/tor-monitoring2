#!/bin/python
from stem import CircStatus
from stem.control import Controller


with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    controller.get_info()
