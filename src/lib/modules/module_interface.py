from abc import ABC, abstractmethod

import threading


class MODULEInterface(ABC):

    def __init__(self, module_name, network_usage):
        super(MODULEInterface, self).__init__()
        self._finished = threading.Event()
        self._network = network_usage
        self._values = []

    @abstractmethod
    def collecting_data(self):
        return

    def sending_data(self, data_name, data_values):
        self._network.send_data("%s: %s" % (data_name,
                                            ("-".join([str(value)
                                             for value in data_values]))))

    def stop(self):
        print("[%s] DISCONNECTING...")
        self._network.disconnect()
        self._finished.set()

    def run(self):
        print("[%s] COLLECTING METRICS...")
        self._network.connect()
        threading.Thread(target=self.collecting_data).start()
