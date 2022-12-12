import json

numb_munc = {0: 'Regla',
             1: 'La Lisa',
             2: 'Playa',
             3: 'Marianao',
             4: 'Boyeros',
             5: 'Arroyo Naranjo',
             6: 'Diez de Octubre',
             7: 'Cerro',
             8: 'Plaza de la Revolución',
             9: 'Centro Habana',
             10: 'Habana Vieja',
             11: 'San Miguel del Padrón',
             12: 'Cotorro',
             13: 'Habana del Este'}

total_pop_per_munc = {'0': 43833,
                      '1': 145023,
                      '2': 178557,
                      '3': 134994,
                      '4': 199633,
                      '5': 205701,
                      '6': 201435,
                      '7': 124646,
                      '8': 141781,
                      '9': 133898,
                      '10': 81313,
                      '11': 159022,
                      '12': 82049,
                      '13': 125702,
                      '14': 174807}

amount_workers_per_munc = {'0': 18688,
                           '1': 64192,
                           '2': 82290,
                           '3': 61992,
                           '4': 84716,
                           '5': 88247,
                           '6': 92020,
                           '7': 57823,
                           '8': 69122,
                           '9': 65372,
                           '10': 41692,
                           '11': 65132,
                           '12': 34377,
                           '13': 50424,
                           '14': 80422}

with open("tests/mmodel/havana_geo_connections/habana_network_geographic.json", 'r') as f:
    edges_json_file = json.load(f)
    new_edges_json = []
    for edge in edges_json_file['graph']['edges']:
        current_perc = edge["metadata"]["weight"]
        munc_source = edge["source"]
        munc_target = edge["target"]
        real_portion_workers = current_perc * \
            amount_workers_per_munc[munc_source]
        real_perc_w = real_portion_workers/total_pop_per_munc[munc_source]
        new_edges_json.append({
            "source": munc_source,
            "target": munc_target,
            "metadata": {"weight": real_perc_w}
        })
    edges_json_file['graph']['edges'] = new_edges_json
    f.close()
with open("tests/mmodel/havana_geo_connections/havana_geo_correct_perc.json", 'w') as f:
    serialized_json = json.dumps(edges_json_file, indent=4)
    f.write(serialized_json)
