from mmodel.calc_params import Initialized
from mmodel.data_reader import Reader
from mmodel.data_cleaner import Cleaner

data_conf_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_conf_mun.xlsx"
data_dead_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_fall_mun.xlsx"


ydata =  Initialized()

cleaner = Cleaner()
reader = Reader()
