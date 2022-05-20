from flask import Flask, render_template, request
import json
import plotly

import model.model

app = Flask(__name__)
D = 0.06
L = 12
T = 150.


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(float(request.args.get('d')), int(request.args.get('l')), int(request.args.get('t')))


@app.route('/')
def index():
    return render_template('index.html', graphJSON=gm(D, L, T))


def gm(D, L, T):
    fig1, fig2 = model.model.calculate([D, L, T])

    graphJSON = {}
    graphJSON['first'] = json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder))
    graphJSON['second'] = json.loads(json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder))

    return json.dumps(graphJSON)


if __name__ == "__main__":
    app.run(debug=True)
