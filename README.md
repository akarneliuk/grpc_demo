# gNMI/Protobuf for network management
This repository contains the Python scripts to work with the:
- Protobuf messages
- gNMI network management

## Operation
The explanation of the demo:

### Protobuf
1. Make sure you have installed `protobuf` toolset, so that you have `protoc` available in your CLI. Details: https://bit.ly/2Lki7Ps
2. Create the Python meta classes out of Protobuf schema file: `protoc -I=. --python_out=. openconfig-interfaces.proto`
3. Generate the Protobuf message using Python 3: `python create_protobuf.py oc_if.bin`
4. Parse the Protobuf message using Python 3: `python read_protobuf.py oc_if.bin`

## Log
Release `0.1`:
- The first release