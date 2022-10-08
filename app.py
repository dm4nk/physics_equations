import json
import os

import numpy as np
import plotly
from flask import Flask, render_template, request

from model.new_model import NewModel
from model.old_model import OldModel
from utils import build_plot

app = Flask(__name__)

old_model = OldModel()
new_model = NewModel()

FILENAME = 'data/data.json'
MINIMAL_T = 0.0001  # approximate minimal T, as it can't be 0, and it should be quite big for fast calculations


@app.route('/draw_plots', methods=['POST', 'GET'])
def draw_plots():
    return gm(float(request.args.get('d')),
              float(request.args.get('l')),
              float(request.args.get('t')),
              float(request.args.get('e')),
              int(request.args.get('x')),
              int(request.args.get('y')))


@app.route('/basic', methods=['POST', 'GET'])
def basic():
    with open(FILENAME, "r", encoding='utf-8') as json_file:
        json_load = json.load(json_file)
        return json_load


@app.route('/')
def index():
    return render_template('index.html')


def gm(d=0.06, l=12., t=150., e=0.01, num_x=500, num_t=500):
    x_ar = np.linspace(0, l, num_x)
    t_ar = np.linspace(0, t, num_t)
    x_values = [0., l / 2, 2 * l / 3, l]
    t_values = [MINIMAL_T, t / 3, 2 * t / 3, t]

    y_old, t_old, t_array, n_array = old_model.set_end_bild(d, l, t, e, x_ar, t_ar, x_values, t_values)
    y_new, t_new = new_model.set_end_bild(d, l, t, e, x_ar, t_ar, x_values, t_values)

    fig1 = build_plot(x_ar, y_old, y_new, t_values, x_label="x", sections_label="t = ")
    fig2 = build_plot(t_ar, t_old, t_new, x_values, x_label="t", sections_label="x = ")

    graph_json = {'first': json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)),
                  'second': json.loads(json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)),
                  't_array': t_array,
                  'n_array': n_array}

    return json.dumps(graph_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
