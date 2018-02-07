window.onload = function() {
    $.ajax({
        type: "GET",
        url: window.location.href + "/statistics",
        success: function(response) {
            var labels = [];
            var values = [];
            jQuery.each(response, function(i, val) {
              jQuery.each(val, function(j, k) {
                  labels.push(j + "-" + i);
                  values.push(k);
              });
            });
            var ctx = document.getElementById('statisticsChart').getContext('2d');
            var chart = new Chart(ctx, {
                // The type of chart we want to create
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "selling statistics",
                        backgroundColor: 'rgb(100, 149, 237)',
                        borderColor: 'rgb(65, 105, 225)',
                        data: values,
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                callback: function(value) {if (value % 1 === 0) {return value;}}
                            }
                        }]
                    }
                }
            });

        },
    });
};
