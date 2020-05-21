$(document).ready(function () {
    var endpoint = $("#allAccountsChart").attr("data-url")
    var labels = [];
    var default_data = [];
    $.ajax({
        method: 'GET',
        url: endpoint,
        success: function (data) {
            labels = data.labels
            default_data = data.chart_data
            setAccountGraph();

        },
        error: function (error_data) {
            console.log(error_data)
        }
    })





    // GRAPH FUNCTIONS

    function setAccountGraph() {
        gradientChartOptionsConfiguration = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },
            tooltips: {
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10
            },
            legend: {
                position: "bottom",
                fillStyle: "#FFF",
                display: false
            },
            responsive: true,
            scales: {
                yAxes: [{
                    display: 0,
                    gridLines: 0,
                    ticks: {
                        display: false,
                        userCallback: function (value, index, values) {
                            return value.toLocaleString();   // this is all we need
                        }
                    },
                    gridLines: {
                        zeroLineColor: "transparent",
                        drawTicks: false,
                        display: false,
                        drawBorder: false
                    }
                }],
                xAxes: [{
                    display: 0,
                    gridLines: 0,
                    ticks: {
                        display: false
                    },
                    gridLines: {
                        zeroLineColor: "transparent",
                        drawTicks: false,
                        display: false,
                        drawBorder: false
                    }
                }]
            },
            layout: {
                padding: {
                    left: 2,
                    right: 2,
                    top: 15,
                    bottom: 0,
                }
            }
        };
        ctx = document.getElementById('allAccountsChart').getContext("2d");

        gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
        gradientStroke.addColorStop(0, '#80b6f4');
        gradientStroke.addColorStop(1, chartColor);

        gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
        gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
        gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

        myChart = new Chart(ctx, {
            type: 'line',
            responsive: true,
            data: {
                labels: labels,
                datasets: [{
                    label: "Available balance",
                    borderColor: "#f96332",
                    pointBorderColor: "#FFF",
                    pointBackgroundColor: "#f96332",
                    pointBorderWidth: 2,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 1,
                    pointRadius: 4,
                    fill: true,
                    backgroundColor: gradientFill,
                    borderWidth: 2,
                    data: default_data
                }]
            },
            options: gradientChartOptionsConfiguration
        });
    }


    // MULTI DATASET

    function setBigChartData() {

        var canvas = document.getElementById("bigChartData");
        var ctx = canvas.getContext('2d');
        var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
        gradientStroke.addColorStop(0, '#80b6f5');
        gradientStroke.addColorStop(1, chartColor);

        var gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
        gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
        gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");

        // Global Options:


        var data = {
            labels: labels_1,
            datasets: [{
                label: "Income",
                borderColor: "#f96332",
                pointBorderColor: "#FFF",
                pointBackgroundColor: "#f96332",
                pointBorderWidth: 2,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 1,
                pointRadius: 4,
                fill: true,
                backgroundColor: gradientFill,
                borderWidth: 2,
                // notice the gap in the data and the spanGaps: true
                data: data_set_1,
                spanGaps: true,
            }, {
                label: "Expense",
                borderColor: chartColor,
                pointBorderColor: chartColor,
                pointBackgroundColor: "#1e3d60",
                pointHoverBackgroundColor: "#1e3d60",
                pointHoverBorderColor: chartColor,
                pointBorderWidth: 1,
                pointHoverRadius: 7,
                pointHoverBorderWidth: 2,
                pointRadius: 5,
                fill: true,
                backgroundColor: gradientFill,
                borderWidth: 2,
                // notice the gap in the data and the spanGaps: false
                data: data_set_2,
                spanGaps: false,
            }

            ]
        };

        // Notice the scaleLabel at the same level as Ticks
        var options = {
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "rgba(255,255,255,0.4)",
                        fontStyle: "bold",
                        beginAtZero: true,
                        maxTicksLimit: 5,
                        padding: 10,

                    },
                    scaleLabel: {

                    },
                    gridLines: {
                        drawTicks: true,
                        drawBorder: false,
                        display: true,
                        color: "rgba(255,255,255,0.1)",
                        zeroLineColor: "transparent"
                    }

                }],
                xAxes: [{
                    gridLines: {
                        zeroLineColor: "transparent",
                        display: false,

                    },
                    ticks: {
                        padding: 10,
                        fontColor: "rgba(255,255,255,0.4)",
                        fontStyle: "bold"
                    }
                }]
            },
            layout: {
                padding: {
                    left: 0,
                    right: 5,
                    top: 0,
                    bottom: 0
                }
            },
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: '#fff',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            legend: {
                position: "bottom",
                fillStyle: "#FFF",
                display: false
            },

        };

        // Chart declaration:
        var myBarChart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: options,
        });
    }

    var big_chart_endpoint = $("#bigChartData").attr("data-url");
    var labels_1 = [];
    var data_set_1 = [];
    var data_set_2 = [];

    $.ajax({
        method: 'GET',
        url: big_chart_endpoint,
        success: function (data) {
            labels_1 = data.label
            data_set_2 = data.expense
            data_set_1 = data.income
            console.log(data);
            setBigChartData();
        },
        error: function () {
            alert('Something Gone wrong')
        }
    });


    // MAIN DASHBOARD CHART

    function setMainDashboardChart() {

        var ctx = document.getElementById('mainDashboardChart').getContext("2d");

        var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
        gradientStroke.addColorStop(0, '#80b6f4');
        gradientStroke.addColorStop(1, chartColor);

        var gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
        gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
        gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");

        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: main_labels,
                datasets: [{
                    label: "Profit",
                    borderColor: chartColor,
                    pointBorderColor: chartColor,
                    pointBackgroundColor: "#1e3d60",
                    pointHoverBackgroundColor: "#1e3d60",
                    pointHoverBorderColor: chartColor,
                    pointBorderWidth: 1,
                    pointHoverRadius: 7,
                    pointHoverBorderWidth: 2,
                    pointRadius: 5,
                    fill: true,
                    backgroundColor: gradientFill,
                    borderWidth: 2,
                    data: [50, 150, 100, 190, 130, 90, 150, 160, 120, 140, 190, 95]
                }]
            },
            options: {
                layout: {
                    padding: {
                        left: 20,
                        right: 20,
                        top: 0,
                        bottom: 0
                    }
                },
                maintainAspectRatio: false,
                tooltips: {
                    backgroundColor: '#fff',
                    titleFontColor: '#333',
                    bodyFontColor: '#666',
                    bodySpacing: 4,
                    xPadding: 12,
                    mode: "nearest",
                    intersect: 0,
                    position: "nearest"
                },
                legend: {
                    position: "bottom",
                    fillStyle: "#FFF",
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            fontColor: "rgba(255,255,255,0.4)",
                            fontStyle: "bold",
                            beginAtZero: true,
                            maxTicksLimit: 5,
                            padding: 10
                        },
                        gridLines: {
                            drawTicks: true,
                            drawBorder: false,
                            display: true,
                            color: "rgba(255,255,255,0.1)",
                            zeroLineColor: "transparent"
                        }

                    }],
                    xAxes: [{
                        gridLines: {
                            zeroLineColor: "transparent",
                            display: false,

                        },
                        ticks: {
                            padding: 10,
                            fontColor: "rgba(255,255,255,0.4)",
                            fontStyle: "bold"
                        }
                    }]
                }
            }
        });
    }

    var main_dash_endpoint = $("#mainDashboardChart").attr("data-url");
    var main_labels = [];
    var main_data = [];

    $.ajax({
        method: 'GET',
        url: main_dash_endpoint,
        success: function (data) {
            main_labels = data.labels
            setMainDashboardChart();
        },
        error: function (error_data) {
            console.log(error_data)
        }
    })
})