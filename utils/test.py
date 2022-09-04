import json
from os import getcwd

numb_munc = {0:'Regla',
1:'La Lisa',
2:'Playa',
3:'Marianao',
4:'Boyeros',
5:'Arroyo Naranjo',
6:'Diez de Octubre',
7:'Cerro',
8:'Plaza de la Revolución',
9:'Centro Habana',
10:'Habana Vieja',
11:'San Miguel del Padrón',
12:'Cotorro',
13:'Habana del Este'}


def extarct_infected_data(people:list):
    d = {}
    for m in numb_munc.values():
        d[m]= len(list(filter(lambda p: p['municipio_detección'] == m ,people['diagnosticados'])))
    return d


with open(f'{getcwd()}/utils/covid19-cuba-1.json','r') as f: 
    json_data = json.load(f)['casos']['dias']
    total_infected = {}
    
    for d in json_data.values():
        infected_in_day = extarct_infected_data(d)
        for mun in infected_in_day:
            try:
                total_infected[mun].append(infected_in_day[mun])
            except KeyError:
                total_infected[mun] = [infected_in_day[mun]] 

    print(total_infected)

