$("document").ready(function () {
    $("#charting").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: "/chart",
            data: $("#charting").serialize(),
            success: function (response, textStatus, jqXHR) {
                var ctx = $("#chart")
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Devis', 'Traductions'],
                        datasets: [{
                            label: 'Statistiques',
                            data: [response['requests'], response['responses']],
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                            }]
                        }
                    }
                });
            }
        });
    });
});
