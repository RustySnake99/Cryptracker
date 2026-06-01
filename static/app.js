let chart;

async function searchCrypto() {
    const coin = document.getElementById("coin-input").value.toLowerCase();
    const response = await fetch(`/crypto/${coin}`);
    const data = await response.json();

    if (data.error) {
        alert("No coin data found.... please check the coin entered!");
        return;
    }
    document.getElementById("result").innerHTML = `
        <div class="card">
            <img src="${data.image}" />
            <h2>${data.name} (${data.symbol.toUpperCase()})</h2>

            <p>
                <ul>
                    <li>Current Price: USD$ ${data.current_price.toLocaleString()}</li>
                    <li>Market Cap: USD$ ${data.market_cap.toLocaleString()}</li>
                    <li>24-Hour High: USD$ ${data.high_24h.toLocaleString()}</li>
                    <li>24-Hour Low: USD$ ${data.low_24h.toLocaleString()}</li>
                    <li>24-Hour Price Change: ${data.price_change_24h.toFixed(2)}%</li>
                </ul>
            </p>
        </div>
    `;
    const labels = data.dates.map(timestamp => {
        return new Date(timestamp).toLocaleString();
    });
    const ctx = document.getElementById("priceChart").getContext("2d");

    if (chart) chart.destroy();
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: `${data.name} Price`,
                data: data.prices,
                borderWidth: 2
            }]
        },
        options: {responsive: true}
    });
}