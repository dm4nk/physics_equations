import json

import plotly
from flask import Flask, render_template, request

from model.model import Model

app = Flask(__name__)

md = Model(0.06, 12, 150, 0.01)


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(float(request.args.get('d')),
              int(request.args.get('l')),
              int(request.args.get('t')),
              float(request.args.get('e')))


@app.route('/')
def index():
    return render_template('index.html', graphJSON=gm())


def gm(d=0.06, l=12, t=150, e=0.01):
    print(d, l, t, e)
    md.set_params(d, l, t, e)
    fig1, fig2 = md.calculate()

    graph_json = {'first': json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)),
                  'second': json.loads(json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder))}

    return json.dumps(graph_json)


if __name__ == "__main__":
    app.run()
