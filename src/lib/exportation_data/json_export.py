import json

from export_pattern import PATTERNExport

class JSONExport(PATTERNExport):
    """docstring for JSONExport"""
    def __init__(self, filename):
        super(JSONExport, self).__init__(filename, "json")

    @PATTERNExport.decor
    def export_data(self, data):
        with open(self._filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent = 4)
