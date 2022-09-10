from pandas import *


class Reader:

    @staticmethod
    def get_data(data_path):
        return read_excel(data_path, sheetname=None)
    

        
