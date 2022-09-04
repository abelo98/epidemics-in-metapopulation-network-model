import json
import pandas as pd


class data_processor:
    def __init__(self, json_data: json) -> None:
        self.json_data = json_data

    def build_dataframe(self):
        df_covid_history = pd.DataFrame([[d.get('day'), 
                                  d['summary'].get('total'), 
                                  d['summary'].get('confirmedCasesIndian'), 
                                  d['summary'].get('confirmedCasesForeign'),
                                  d['summary'].get('confirmedButLocationUnidentified'),
                                  d['summary'].get('discharged'), 
                                  d['summary'].get('deaths')] 
                                 for d in covid_history],
                    columns=keys)