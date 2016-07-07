import csv

from exportation_interface import EXPORTModule


class CSVExport(EXPORTModule):
    """docstring for CSVExport"""
    def __init__(self, filename):
        super(CSVExport, self).__init__(filename, "csv")

    @EXPORTModule.decor
    def export_data(self, data):
        with open(self._filename, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for single_data in data:
                csvwriter.writerow(list(single_data))
