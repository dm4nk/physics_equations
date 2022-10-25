const submitBtn = document.querySelector('.submit-btn');
submitBtn.addEventListener('click', function (event) {
    event.preventDefault();
    const c = parseFloat(document.querySelector('#c').value);
    const k = parseFloat(document.querySelector('#k').value);
    const a = parseFloat(document.querySelector('#a').value);
    const l = parseFloat(document.querySelector('#l').value);
    const r = parseFloat(document.querySelector('#r').value);
    const t = parseFloat(document.querySelector('#t').value);
    const r_dis = parseFloat(document.querySelector('#r_dis').value);
    const t_dis = parseFloat(document.querySelector('#t_dis').value);

    if (c == null || k == null || a == null || l == null || r == null || t == null || r_dis == null || t_dis == null) {
        alert("validation failed");
        return;
    }

    submitBtn.disabled = true;
    submitBtn.classList.remove('gradient-background');

    console.log('START');

    $.getJSON({
        url: "/draw_plots",
        data: {
            'c': c,
            'k': k,
            'a': a,
            'l': l,
            'r': r,
            't': t,
            'r_dis': r_dis,
            't_dis': t_dis,
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
        },
        error: function (result) {
             alert("Bad parameters. Try again");
        }
    });
});