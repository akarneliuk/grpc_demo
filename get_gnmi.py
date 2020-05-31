#!/usr/bin/env python

# Modules
import grpc
from bin.gnmi_pb2_grpc import *
from bin.gnmi_pb2 import *
import re
import sys
import json


# Variables
path = {'inventory': 'inventory/inventory.json', 'network_functions': 'inventory/network_functions'}


# User-defined functions
def json_to_dict(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


def gnmi_path_generator(path_in_question):
    gnmi_path = Path()

    path_elements = path_in_question.split('/')

    for pe_entry in path_elements:
        if not re.match('.+?:.+?', pe_entry) and len(path_elements) == 1:
            sys.exit(f'You haven\'t specified either YANG module or the top-level container in \'{pe_entry}\'.')

        elif re.match('.+?:.+?', pe_entry):
            gnmi_path.origin = pe_entry.split(':')[0]
            gnmi_path.elem.add(name=pe_entry.split(':')[1])

        elif re.match('.+?\[.+?\]', pe_entry):
            gnmi_path.elem.add(name=pe_entry.split('[')[0], key={f'{pe_entry.split("[")[1].split("=")[0]}': f'{re.sub("]", "", pe_entry.split("[")[1].split("=")[1])}'})

        else:
            gnmi_path.elem.add(name=pe_entry)

    return gnmi_path


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
