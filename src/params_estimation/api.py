from unittest import result
from mmodel.simple_trip import SimpleTripMetaModel


class ApiConn:
    def __init__(self,model_name:str, file_path:str) -> None:
        self.model = SimpleTripMetaModel(model_name, file_path)
        self.output_simulation = None

    def simulate(self,input_params, input_time):
        self.output_simulation = self.model.simulate(input_params, input_time)