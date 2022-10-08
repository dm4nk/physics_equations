import plotly.graph_objects as go


def build_plot(x: [float], old_y_arrays: [float], new_y_arrays: [[float]], sections: [float], x_label: [str],
               sections_label: [str]) \
        -> go.Figure:
    """
    Builds plot for given parameters
    :param new_y_arrays: y calculated with new model
    :param old_y_arrays: y calculated with old model
    :param sections_label:
    :param x_label:
    :param x: x from
    :param sections: sections
    """
    fig = go.Figure()
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
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
    for old_y, new_y, section in zip(old_y_arrays, new_y_arrays, sections):
        fig.add_trace(
            go.Line(x=x, y=new_y, mode='lines', name=sections_label + str(section))
        )

        fig.add_trace(
            go.Scatter(x=x, y=old_y, name=sections_label + str(section), line=dict(width=4, dash='dash'))
        )

    return fig
