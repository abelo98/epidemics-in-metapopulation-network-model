from ..simple_trip import SimpleTripMetaModel


class ApiConn:
    def __init__(self, model_name: str, file_path: str) -> None:
        self.model = SimpleTripMetaModel(model_name, file_path)
        self.output_simulation = None

    def simulate(self, input_params, input_time):
        self.output_simulation = self.model.simulate(input_params, input_time)

    def get_ydata_for_node(self, idx: int, compartiments: list):
        for compart in compartiments:
            yield self.output_simulation[idx][compart]

    def transform_input(self, initial_v):
        initial_v_extended, _ = self.model.__transform_input__(initial_v, None)
        return initial_v_extended

    def read_json_node(self, nodes_json):
        return self.model.import_input(nodes_json)
