from Connection import PYATSConnection
testbed = "development.yaml"

def update_port_vlan(vlan, interface, device_ip, mode):
    connection = PYATSConnection(testbed=testbed)
    if mode == "access":
        updated_interface = [f"interface {interface}\nswitchport mode access\nswitchport access vlan {vlan}"]
    elif mode == "trunk":
        pass

    connection.update_device_running_config(ip=device_ip, configuration=updated_interface)


def copy_port_config(device_ip, source_port, destination_port):
    source_config = []
    connection = PYATSConnection(testbed=testbed)
    device_config = connection.get_device_running_config(device_ip)
    interface = device_config[f'interface {source_port}']
    source_config.append(f'interface {destination_port}')
    for config in interface:
        print(config)
        source_config.append(config)

    connection.update_device_running_config(device_ip, ["\n".join(source_config)])



def assign_vlan_ip_address(vlan, device_ip, ip_assignment, subnet_assignment):
    connection = PYATSConnection(testbed=testbed)
    updated_vlan = [f"interface Vlan{vlan}\nip address {ip_assignment} {subnet_assignment}"]
    connection.update_device_running_config(ip=device_ip,configuration=updated_vlan)

