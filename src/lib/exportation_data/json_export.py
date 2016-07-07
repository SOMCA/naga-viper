import json

from exportation_interface import EXPORTModule


class JSONExport(EXPORTModule):
    """docstring for JSONExport"""
    def __init__(self, filename):
        super(JSONExport, self).__init__(filename, "json")

    @EXPORTModule.decor
    def export_data(self, data):
        with open(self._filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
