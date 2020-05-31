# gNMI/Protobuf for network management
This repository contains the Python scripts to work with the:
- Protobuf messages
- gNMI network management

## Operation
The explanation of the demo:

### Protobuf
1. Make sure you have installed `protobuf` toolset, so that you have `protoc` available in your CLI. Details: https://bit.ly/2Lki7Ps
2. Create the Python meta classes out of Protobuf schema file: `protoc -I=bin --python_out=bin openconfig-interfaces.proto`
3. Generate the Protobuf message using Python 3: `python create_protobuf.py oc_if.bin`
4. Parse the Protobuf message using Python 3: `python read_protobuf.py oc_if.bin`

## Log
Release `0.3.1`:
- Modified the structure of the files so that inventory are moved to a directory `inventory`, which has subfolder `network_functions` with per device data.

Release `0.3.0`:
- The file `act_gnmi.py` is renamed to `get_gnmi.py`.
- The new file `set_gnmi.py` is created to perform the configuration of the network elements via gRPC transport with gNMI specification and OpenConfig YANG modules.

Release `0.2.3`:
- Minor bug fixing with the encodign, as Nokia doesn't support `JSON_IETF`.
- Added the devices configuration folder `nf_config`.

Release `0.2.2`:
- Minor bug fixing with the `gnmi_path_generator` function.

Release `0.2.1`:
- Added the Python script `act_gnmi.py`, which collects the information per gNMI specification using the gRPC transport.
- Added the `topology` folder, which explains the lab setup.

Release `0.2.0`:
- Modified the `requirements.txt` to include the `grpcio` and `grpcio-tools`.

Release `0.1.2`:
- Minor bug fixing in `read_protobuf.py`.

Release `0.1.1`:
- Restructured the files hierarchy by adding `bin` and `messages` directories.
- Modified the `create_protobuf.py` and `read_protobuf.py` to work with new files' structure.

Release `0.1`:
- The first release
