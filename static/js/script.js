$.getJSON({
    url: "/basic",
    success: function (result) {
        Plotly.newPlot('chart', result['first'], {
            staticPlot: true
        });
        Plotly.newPlot('chart2', result['second'], {
            staticPlot: true
        });
    }
});

const submitBtn = document.querySelector('.submit-btn');
submitBtn.addEventListener('click', function (event) {
    const d = parseFloat(document.querySelector('#d').value);
    const l = parseFloat(document.querySelector('#l').value);
    const t = parseFloat(document.querySelector('#t').value);
    const x = parseFloat(document.querySelector('#x').value);
    const y = parseFloat(document.querySelector('#y').value);

    if (d == null || l == null || t == null || x == null || y == null) {
        alert("validation failed");
        return;
    }

    submitBtn.disabled = true;
    submitBtn.classList.remove('gradient-background');

    event.preventDefault();
    console.log('START');

    $.getJSON({
        url: "/draw_plots",
        data: {
            'd': d,
            'l': l,
            't': t,
            'x': x,
            'y': y
        },
        success: function (result) {
            Plotly.newPlot('chart', result['first'], {
                staticPlot: true
            });
            Plotly.newPlot('chart2', result['second'], {
                staticPlot: true
            });

            submitBtn.disabled = false;
            submitBtn.classList.add('gradient-background');
            console.log('REFRESHED');
        }
    });
});