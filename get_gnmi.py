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
    keys = []

    while re.match('.*?\[.+?=.+?\].*?', path_in_question):
        temp_key, temp_value = re.sub('.*?\[(.+?)\].*?', '\g<1>', path_in_question).split('=')
        keys.append({temp_key: temp_value})
        path_in_question = re.sub('(.*?\[).+?(\].*?)', f'\g<1>{len(keys) - 1}\g<2>', path_in_question)

    print(keys)
    print(path_in_question)

    path_elements = path_in_question.split('/')

    for pe_entry in path_elements:
        if not re.match('.+?:.+?', pe_entry) and len(path_elements) == 1:
            sys.exit(f'You haven\'t specified either YANG module or the top-level container in \'{pe_entry}\'.')

        elif re.match('.+?:.+?', pe_entry):
            gnmi_path.origin = pe_entry.split(':')[0]
            gnmi_path.elem.add(name=pe_entry.split(':')[1])

        elif re.match('.+?\[\d+?\].*?', pe_entry):
            key_id = int(re.sub('.+?\[(\d+?)\].*?', '\g<1>', pe_entry))
            gnmi_path.elem.add(name=pe_entry.split('[')[0], key=keys[key_id])

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
