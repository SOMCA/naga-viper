import threading

from datetime import timedelta
from socket import socket
from time import time

from yoctopuce.yocto_api import YAPI, YRefParam, YModule
from yoctopuce.yocto_current import YCurrent

class YoctoDevice(object):
    """Class to instantiate an ammeter device"""

    QUIT_STATE = "QUIT"
    DATA_STATE = "DATA"
    NAME_STATE = "NAME"

    def __init__(self, framerate, network_usage = None):
        super(YoctoDevice, self).__init__()

        try:
            # check the ammeter
            self._device = YCurrent.FindCurrent(".".join([self.serialNumber, 'current1']))
            if not self._device and not self.module.isOnline():
                raise Exception('Could not get sensor device from ' + ammeter_serialnumber)
            self._device.set_reportFrequency(framerate)
            self._device.registerTimedReportCallback(self.addMeasure)
            self._finished = threading.Event()
            self._init_time = None
            self._values = []
            self._network = network_usage
        except Exception as init_exception:
            raise init_exception

    def __repr__(self):
        ammeter_info = [
            "* Yocto ammeter %r (uptime %r)" % (self.serialNumber, self.uptime),
            "---> Hardware ID: %r" % self.hardwareId,
            "---> Logical name: %r" % self.logicalName,
            "---> USB consumption: %r mA" % self.usbConsumption,
            "---> BEACON state: %r" % self.beacon,
        ]
        return "\n".join(ammeter_info)

    def addMeasure(self, fct, measure):
        current_time = (time() - self._init_time)
        data_to_store = ("{:2.3f}".format(current_time),
                         measure.get_averageValue())
        if self._network:
            self._network.send_data("%s %s" % (DATA_STATE,
                                               ("-".join([str(value)
                                                for value in data_to_store]))))
        self._values.append(data_to_store)

    def stopMeasure(self):
        # Close the server automatically
        if self._network:
            self._network.send_data(QUIT_STATE)
        self._finished.set()

    def launchMeasure(self):
        self._init_time = time()
        while not self._finished.isSet():
            YAPI.Sleep(500)
        print("Process finished!")

    def sendDataName(self):
        if self._network:
            self._network.send_data("%s %s" % (NAME_STATE, self._name))

    @property
    def module(self):
        # check if the module is already instantiated
        if hasattr(self, '_module') and self._module:
            return self._module
        # check if the ammeter is attached by USB
        errmsg = YRefParam()
        if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
            raise Exception("Could not register the yocto device with USB connection.")

        ammeter = YCurrent.FirstCurrent()
        # find the ammeter
        if not ammeter:
            raise Exception("Could not find the yocto device.")
        # check if the ammeter is online
        if not ammeter.isOnline():
            raise Exception("Your ammeter device is not currently reachable.")
        # initialize the ammeter and return this one
        self._module = ammeter.get_module()
        return self._module

    @property
    def serialNumber(self):
        if hasattr(self, '_serial_number') and self._serial_number:
            return self._serial_number
        self._serial_number = self.module.get_serialNumber()
        return self._serial_number

    @property
    def hardwareId(self):
        if hasattr(self, '_hardware_id') and self._hardware_id:
            return self._hardware_id
        self._hardware_id = self.module.get_hardwareId()
        return self._hardware_id

    @property
    def logicalName(self):
        if hasattr(self, '_logical_name') and self._logical_name:
            return self._logical_name
        self._logical_name = self.module.get_logicalName()
        return self._logical_name

    @property
    def usbConsumption(self):
        return self.module.get_usbCurrent()

    @property
    def uptime(self):
        return str(timedelta(milliseconds = self.module.get_upTime()))

    @property
    def beacon(self):
        if hasattr(self, '_beacon') and self._beacon:
            return self._beacon
        self._beacon = self.module.get_beacon()
        return self._beacon

    @beacon.setter
    def beacon(self, boolean):
        self.module.set_beacon(YModule.BEACON_ON if boolean
                                                 else YModule.BEACON_OFF)

    def run(self):
        # check if the thread has been done or not...
        print("Launching runs...")
        if self._network:
            self._network.connect()
        threading.Thread(target=self.launchMeasure).start()
        if self._network:
            self._network.disconnect()
