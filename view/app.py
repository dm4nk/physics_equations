import math

import numpy
from flask import Flask, render_template
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from Constants import Constants
from model.model import u

app = Flask(__name__)

T = Constants.D.value
L = Constants.L.value


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    mu_array = [i * math.pi for i in range(1, 101)]

    x = numpy.linspace(0, L, 500)

    y1 = [u(_x, 0, mu_array) for _x in x]
    y2 = [u(_x, T / 3, mu_array) for _x in x]
    y3 = [u(_x, 2 * T / 3, mu_array) for _x in x]
    y4 = [u(_x, T, mu_array) for _x in x]

    axis.plot(x, y1, label="t = 0")
    axis.plot(x, y2, label="t = T/3")
    axis.plot(x, y3, label="t = 2*T/3")
    axis.plot(x, y4, label="t = T")

    # axis.xlabel("t")
    # axis.ylabel("U(mu, t)")
    # axis.legend()
    return fig


@app.route("/")
def crate_plot():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    # return Response(output.getvalue(), mimetype='image/png')
    return render_template('index.html', name = 'new_plot', url ='/static/templates/index.png')

