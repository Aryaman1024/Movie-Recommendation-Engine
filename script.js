const chartData = JSON.parse(document.getElementById("chart-data").textContent);

const labels = Object.keys(chartData);
const values = Object.values(chartData);

const ctx = document.getElementById("chart");

// 🔥 destroy previous chart (important fix)
if (window.myChart) {
    window.myChart.destroy();
}

// 🔥 create new chart (same style as before)
window.myChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: labels,
        datasets: [{
            label: "Movies per Genre",
            data: values,
            backgroundColor: [
                "#4CAF50",
                "#2196F3",
                "#FF9800",
                "#9C27B0",
                "#00BCD4",
                "#FFC107",
                "#8BC34A",
                "#FF5722",
                "#795548",
                "#607D8B"
            ],
            borderRadius: 6
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: "#ccc"
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: "#aaa"
                }
            },
            y: {
                ticks: {
                    color: "#aaa"
                }
            }
        }
    }
});

function searchMovie() {
    let input = document.getElementById("searchInput").value.toUpperCase();
    let table = document.getElementById("movieTable");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            let text = td.textContent || td.innerText;
            tr[i].style.display = text.toUpperCase().includes(input) ? "" : "none";
        }
    }
}