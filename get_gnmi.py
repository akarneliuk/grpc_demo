#!/usr/bin/env python

# Modules
import grpc
from bin.gnmi_pb2_grpc import *
from bin.gnmi_pb2 import *
import re
import sys
import json


# Own modules
from bin.PathGenerator import gnmi_path_generator


# Variables
path = {'inventory': 'inventory/inventory.json', 'network_functions': 'inventory/network_functions'}


# User-defined functions
def json_to_dict(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


# Body
if __name__ == '__main__':
    inventory = json_to_dict(path['inventory']) 

    for td_entry in inventory['network_functions']:
        metadata = [('username', td_entry['username']), ('password', td_entry['password'])]

        grpc_connection = grpc.insecure_channel(f'{td_entry["ip_address"]}:{td_entry["port"]}', metadata)
        grpc.channel_ready_future(grpc_connection).result(timeout=5)

        gnmi_interface = gNMIStub(grpc_connection)

        device_data = json_to_dict(f'{path["network_functions"]}/{td_entry["hostname"]}.json')

        gnmi_message = []
        for itc_entry in device_data['intent_config']:
            print(f'Setting data for the {itc_entry} data from {td_entry["ip_address"]} over gNMI...\n\n')

            intent_path = gnmi_path_generator(itc_entry['path'])

            gnmi_message.append(intent_path)

        gnmi_message_request = GetRequest(path=gnmi_message, type=0, encoding=0)
        gnmi_message_response = gnmi_interface.Get(gnmi_message_request, metadata=metadata)

        print(gnmi_message_response)
