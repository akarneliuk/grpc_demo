#!/usr/bin/env python

# Modules
import openconfig_interfaces_pb2
import sys

# User-defined functions
def parse_protobuf(obj):
    temp_dict = {}
    temp_dict['interface'] = []

    for interface_entry in obj.interface:

        temp_cont = {}
        temp_cont['name'] = interface_entry.name
        temp_cont['config'] = {}
        temp_cont['config']['name'] = interface_entry.config.name
        temp_cont['config']['type'] = interface_entry.config.type
        temp_cont['config']['mtu'] = interface_entry.config.mtu
        temp_cont['config']['description'] = interface_entry.config.description
        temp_cont['config']['enabled'] = interface_entry.config.enabled
        temp_cont['config']['subinterfaces'] = {'subinterface': []}

        for siface_entry in interface_entry.subinterfaces.subinterface:
            temp_sub_cont = {}

            temp_sub_cont['index'] = siface_entry.index
            temp_sub_cont['config'] = {}
            temp_sub_cont['config']['index'] = siface_entry.config.index
            temp_sub_cont['config']['description'] = siface_entry.config.description
            temp_sub_cont['config']['enabled'] = siface_entry.config.enabled

            temp_cont['config']['subinterfaces']['subinterface'].append(temp_sub_cont)


        temp_dict['interface'].append(temp_cont)

    return temp_dict


# Body
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Using {sys.argv[0]} as file.')
        sys.exit(-1)

    oc_if = openconfig_interfaces_pb2.Interfaces()

    with open(sys.argv[1], "rb") as f:
        oc_if.ParseFromString(f.read())

    parsed_data = parse_protobuf(oc_if)

    print(parsed_data)