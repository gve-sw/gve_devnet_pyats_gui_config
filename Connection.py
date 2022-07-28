from genie.testbed import load
from prettyprinter import pprint
import traceback

class PYATSConnection:
    def __init__(self, testbed="development"):
        # self.__devices_regions = create_testbed()
        print(testbed)
        self.__testbed = load(f"./testbeds/{testbed}")
        self.__devices = self.__find_device_by_ip()



    def __find_device_by_ip(self):
        devices = {}
        for device_name, device in self.__testbed.devices.items():
            devices[str(device.connections['ssh']['ip'])] = device

        print(devices)

        return devices

    def get_device_running_config(self, ip):
        if ip in self.__devices.keys():
            try:
                print(ip)
                pprint(self.__devices[ip])
                device = self.__devices[ip]
                device.connect(learn_os=True, init_config_commands=[])
                return device.learn('config')
            except Exception as e:
                print(f"An error has occured while trying to connect to the following Device IP: {ip}")
                print(traceback.format_exc())
                print(e)




        else:
            print(f"Device IP \"{ip}\" not found in testbed!")
            return None




    def update_device_running_config(self, ip, configuration):
        if not configuration:
            return False
        if ip in self.__devices.keys():
            try:
                device = self.__devices[ip]
                device.connect(learn_os=True, init_config_commands=[])
                for command in configuration:
                    device.configure(command)

                return True


            except Exception as e:
                print(f"An error has occured while trying to connect to the following Device IP: {ip}")
                print(e)
                return False


            finally:
                device.disconnect()




        else:
            print(f"Device IP \"{ip}\" not found in testbed!")
            return None


    def get_devices_in_testbed(self):
        return self.__devices


