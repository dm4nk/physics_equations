import json
import os

import numpy as np
import plotly
from flask import Flask, render_template, request

from model.new_model import NewModel
from utils import build_plot

app = Flask(__name__)

new_model = NewModel()


@app.route('/draw_plots', methods=['POST', 'GET'])
def draw_plots():
    return gm(C=float(request.args.get('c')),
              K=float(request.args.get('k')),
              A=float(request.args.get('a')),
              L=float(request.args.get('l')),
              R=float(request.args.get('r')),
              T=float(request.args.get('t')),
              num_x=int(request.args.get('r_dis')),
              num_t=int(request.args.get('t_dis')))


@app.route('/basic', methods=['POST', 'GET'])
def basic():
    return data.initial_plot


@app.route('/')
def index():
    return render_template('index.html')


def gm(C=2.64, R=3., T=80., K=0.13, A=0.002, L=0.5, num_x=500, num_t=500):
    x_ar = np.linspace(0, R, num_x)
    t_ar = np.linspace(0, T, num_t)
    x_values = [0., R / 2, 2 * R / 3, R]
    t_values = np.linspace(0, T, 4)

    y_new, t_new = new_model.set_end_bild(C=C, R=R, T=T, K=K, A=A, L=L, X=x_ar, Y=t_ar, X_VALS=x_values,
                                          T_VALS=t_values)

    fig1 = build_plot(x_ar, y_new, t_values, x_label="x", sections_label="t = ")
    fig2 = build_plot(t_ar, t_new, x_values, x_label="t", sections_label="x = ")

    graph_json = {'first': json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)),
                  'second': json.loads(json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder))}

    return json.dumps(graph_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
