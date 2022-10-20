import plotly.graph_objects as go


def build_plot(x: [float], new_y_arrays: [[float]], sections: [float], x_label: [str],
               sections_label: [str]) \
        -> go.Figure:
    """
    Builds plot for given parameters
    :param new_y_arrays: y calculated with model
    :param sections_label:
    :param x_label:
    :param x: x from
    :param sections: sections
    """
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(
            showgrid=True,
            showline=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            gridcolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside'
        ),
        yaxis=dict(
            showgrid=True,
            showline=False,
            zeroline=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            gridcolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside'
        ),
        autosize=True,
        margin=dict(
            autoexpand=True,
            l=100,
            r=100,
            t=110,
        ),
        showlegend=True,
        plot_bgcolor='white'
    )
    fig.update_layout(xaxis_title=x_label, yaxis_title="U(x, t)")
    for new_y, section in zip(new_y_arrays, sections):
        fig.add_trace(
            go.Line(x=x, y=new_y, mode='lines', name=sections_label + "{:10.1f}".format(section))
        )

    return fig
