#!/usr/bin/env python

# Modules
import grpc
from bin.gnmi_pb2_grpc import *
from bin.gnmi_pb2 import *
import re
import sys
import json


# Variables
info_to_collect = ['openconfig-interfaces:interfaces/interface[name=Ethernet2]']
target_devices = [
                    {
                        'ip_address': '192.168.100.62',
                        'port': 6030,
                        'username': 'aaa',
                        'password': 'aaa'
                    }
                 ]


# User-defined functions
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
    for td_entry in target_devices:
        metadata = [('username', td_entry['username']), ('password', td_entry['password'])]

        grpc_connection = grpc.insecure_channel(f'{td_entry["ip_address"]}:{td_entry["port"]}', metadata)
        grpc.channel_ready_future(grpc_connection).result(timeout=5)

        gnmi_interface = gNMIStub(grpc_connection)

        for itc_entry in info_to_collect:
            print(f'Setting data for the {itc_entry} data from {td_entry["ip_address"]} over gNMI...\n\n')

            intent_path = gnmi_path_generator(itc_entry)

            intent_config = json.dumps({'config': {'enabled': True, 'type': 'iana-if-type:ethernetCsmacd', 'description': 'ABC'}}).encode('utf-8')

            gnmi_update_message = Update(path=intent_path, val=TypedValue(json_val=intent_config))
            gnmi_message_request = SetRequest(update=[gnmi_update_message])
            gnmi_message_response = gnmi_interface.Set(gnmi_message_request, metadata=metadata)

            print(gnmi_message_response)
