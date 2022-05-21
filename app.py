from flask import Flask, render_template, request
import json
import plotly

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


def gm(D=0.06, L=12, T=150, EPS=0.01):
    print(D, L, T, EPS)
    md.set_params(D, L, T, EPS)
    fig1, fig2 = md.calculate()

    graphJSON = {}
    graphJSON['first'] = json.loads(json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder))
    graphJSON['second'] = json.loads(json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder))

    return json.dumps(graphJSON)


if __name__ == "__main__":
    app.run(debug=True)
