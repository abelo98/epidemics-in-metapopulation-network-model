from pandas import *


class Reader:
    def __init__(self, data_path: str) -> None:
        self._data_path = data_path

    def get_data(self):
        return read_excel(self._data_path, sheetname=None)
    

        
