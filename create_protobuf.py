#!/usr/bin/env python

# Modules
import bin.openconfig_interfaces_pb2 as openconfig_interfaces_pb2
import sys

# Variable
path_messages = 'messages'
intend = {
            'interfaces': {
                'interface': [
                    {
                        'name': 'Ethernet1',
                        'config': {
                            'name': 'Ethernet1',
                            'type': 'ethernetCsmcsd',
                            'mtu': 1514,
                            'description': 'ABC',
                            'enabled': True
                        },
                        'subinterfaces': {
                            'subinterface': [
                                {
                                    'index': 0,
                                    'config': {
                                        'index': 0,
                                        'description': 'DEF',
                                        'enabled': True
                                    }
                                }
                            ]
                        }
                    },
                    {
                        'name': 'Ethernet2',
                        'config': {
                            'name': 'Ethernet2',
                            'type': 'ethernetCsmcsd',
                            'mtu': 1514,
                            'description': '123',
                            'enabled': True
                        },
                        'subinterfaces': {
                            'subinterface': [
                                {
                                    'index': 0,
                                    'config': {
                                        'index': 0,
                                        'description': '456',
                                        'enabled': True
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
         }


# User-defined functions
def build_protobuf(data):
    obj = openconfig_interfaces_pb2.Interfaces()

    for interface_entry in data['interfaces']['interface']:
        iface = obj.interface.add(name=interface_entry['name'])

        iface.config.name = interface_entry['config']['name']

        if interface_entry['config']['type'] == 'ethernetCsmcsd':
            iface.config.type = openconfig_interfaces_pb2.InterfaceType.ethernetCsmcsd
            
        iface.config.mtu = interface_entry['config']['mtu']
        iface.config.description = interface_entry['config']['description']
        iface.config.enabled = interface_entry['config']['enabled']

        for sif_entry in interface_entry['subinterfaces']['subinterface']:
            siface = iface.subinterfaces.subinterface.add(index=sif_entry['index'])
            siface.config.index = sif_entry['config']['index']
            siface.config.description = sif_entry['config']['description']
            siface.config.enabled = sif_entry['config']['enabled']

    return obj

# Body
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Using {sys.argv[0]} as file.')
        sys.exit(-1)

    oc_if = build_protobuf(intend)

    with open(f'{path_messages}/{sys.argv[1]}', "wb") as f:
        f.write(oc_if.SerializeToString())