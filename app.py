import json
import os

import plotly
from flask import Flask, render_template, request

from model.model import Model

app = Flask(__name__)

md = Model(0.06, 12, 150, 0.01)

FILENAME = 'data/data.json'


@app.route('/draw_plots', methods=['POST', 'GET'])
def draw_plots():
    return gm(float(request.args.get('d')),
              float(request.args.get('l')),
              float(request.args.get('t')),
              float(request.args.get('e')))


@app.route('/basic', methods=['POST', 'GET'])
def basic():
    with open(FILENAME, "r", encoding='utf-8') as json_file:
        json_load = json.load(json_file)
        return json_load


@app.route('/')
def index():
    return render_template('index.html')


def gm(d=0.06, l=12., t=150., e=0.01):
    print(d, l, t, e)
    md.set_params(d, l, t, e)
    fig1, fig2, t_array, n_array = md.build_plots()

    graph_json = {'first': json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)),
                  'second': json.loads(json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)),
                  't_array': t_array,
                  'n_array': n_array}

    return json.dumps(graph_json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
