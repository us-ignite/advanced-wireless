var chart = {
    render: function (data) {
        nv.addGraph(function () {
            var chart = nv.models.pieChart()
                .x(function (d) {
                    return d.label
                })
                .y(function (d) {
                    return d.value
                })
                .showLabels(false);
            // Use integers in the values:
            chart.valueFormat(d3.format('d'));

            d3.select("#chart__stage svg")
                .datum(data.apps.stage.concat(data.ac.stage))
                .transition().duration(350)
                .call(chart);
console.log(data.ac.domain);
            d3.select("#chart__domain svg")
                .datum(data.apps.domain.concat(data.ac.domain))
                .transition().duration(350)
                .call(chart);

            d3.select("#chart__feature svg")
                .datum(data.apps.feature.concat(data.ac.feature))
                .transition().duration(350)
                .call(chart);

            d3.selectAll('.nv-slice')
                .on('click', function (d, i) {
                    console.log(d.data.url)
                    window.location.href = d.data.url;
                });

            return chart;
        });
    }
};
