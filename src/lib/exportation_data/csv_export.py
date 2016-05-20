import csv

from export_pattern import PATTERNExport

class CSVExport(PATTERNExport):
    """docstring for CSVExport"""
    def __init__(self, filename):
        super(CSVExport, self).__init__(filename, "csv")

    @PATTERNExport.decor
    def export_data(self, data):
        with open(self._filename, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for single_data in data:
                csvwriter.writerow(list(single_data))
