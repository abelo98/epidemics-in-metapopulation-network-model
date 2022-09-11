from mmodel.calc_params import initialize
from mmodel.data_reader import Reader
from mmodel.data_cleaner import Cleaner

import numpy as np

data_conf_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_conf_mun.xlsx"
data_dead_path = "/media/abel/TERA/School/5to/tesis stuff/cv19_fall_mun.xlsx"

muncps = ["Playa",
          "Plaza de la Revolución",
          "Centro Habana",
          "La Habana Vieja",
          "Regla",
          "La Habana del Este",
          "Guanabacoa",
          "San Miguel del Padrón",
          "Diez de Octubre",
          "Cerro",
          "Marianao",
          "La Lisa",
          "Boyeros",
          "Arroyo Naranjo",
          "Cotorro"]

ydata = initialize()

df_conf = Reader.get_data(data_conf_path)
df_dead = Reader.get_data(data_dead_path)

df_conf_havana = Cleaner.select_rows(df_conf, muncps)
df_dead_havana = Cleaner.select_rows(df_dead, muncps)

df_infected_havana = {
    key: abs(np.subtract(df_conf_havana[key], df_dead_havana[key])) for key in df_conf_havana}

print("end")


N = 1.0
I0 = ydata[0]
S0 = N - I0
R0 = 0.0