import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from mmodel.mmodel import MetaModel
from typing import Dict


def show_simulation(model: MetaModel, result: Dict, time: np.ndarray):
    cmodel = get_compartimental_model_type(model).lower()
    if cmodel in {"sir", "sirs"}:
        return show_sir_simulation(model, result, time)

    if cmodel == "sis":
        return show_sis_simulation(model, result, time)

    raise NotImplementedError(
        f"No visualization for {cmodel} compartimental models")


def show_sir_simulation(model: MetaModel, result: Dict, time: np.ndarray):
    s, i, r = (0, 0, 0)
    for node in model.network.nodes:
        idx = node.id
        s += result[idx]["S"]
        i += result[idx]["I"]
        r += result[idx]["R"]

    figure = make_subplots(rows=3, cols=1)
    figure.append_trace(go.Scatter(
        x=time, y=s, mode="lines", name="S"), row=1, col=1)
    figure.append_trace(go.Scatter(
        x=time, y=i, mode="lines", name="I"), row=2, col=1)
    figure.append_trace(go.Scatter(
        x=time, y=r, mode="lines", name="R"), row=3, col=1)

    return figure


def show_sis_simulation(model: MetaModel, result: Dict, time: np.ndarray):
    s, i = 0, 0
    for node in model.network.nodes:
        idx = node.id
        s += result[idx]["S"]
        i += result[idx]["I"]

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=time, y=s, mode="lines", name="S"))
    figure.add_trace(go.Scatter(x=time, y=i, mode="lines", name="I"))
    return figure


def get_compartimental_model_type(model: MetaModel) -> str:
    return model.network.nodes[0].cmodel
