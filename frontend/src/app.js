const formatter = new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 2
});

let mortgages = [];
let chartInstance = null;
let currentId = 0;

const COLORS = [
    '#6366f1', // Indigo
    '#10b981', // Emerald
    '#f43f5e', // Rose
    '#f59e0b', // Amber
    '#8b5cf6', // Violet
    '#06b6d4', // Cyan
];

document.getElementById('btn-calcular').addEventListener('click', async () => {
    const capital = parseFloat(document.getElementById('capital').value);
    const interesAnual = parseFloat(document.getElementById('interes').value);
    const plazoAnios = parseInt(document.getElementById('plazo').value, 10);
    const errorMsg = document.getElementById('error-msg');

    errorMsg.textContent = "";

    if (isNaN(capital) || isNaN(interesAnual) || isNaN(plazoAnios) || capital <= 0 || plazoAnios <= 0 || interesAnual < 0) {
        errorMsg.textContent = "Por favor, introduce valores numéricos válidos y mayores a cero.";
        return;
    }

    try {
        const response = await fetch('/api/calcular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                capital: capital,
                interes_anual: interesAnual,
                plazo_anios: plazoAnios
            })
        });

        if (!response.ok) {
            throw new Error(`Error en el servidor: ${response.status}`);
        }

        const data = await response.json();
        const color = COLORS[currentId % COLORS.length];

        mortgages.push({
            id: currentId++,
            params: { capital, interesAnual, plazoAnios },
            results: data,
            color: color
        });

        render();

    } catch (error) {
        console.error("Error al calcular:", error);
        errorMsg.textContent = "Ha ocurrido un error al conectar con el servidor.";
    }
});

function removeMortgage(id) {
    mortgages = mortgages.filter(m => m.id !== id);
    render();
}

function render() {
    renderCards();
    renderChart();
}

function renderCards() {
    const container = document.getElementById('mortgage-cards-container');
    container.innerHTML = ''; 

    if (mortgages.length === 0) {
        container.innerHTML = '<p class="empty-msg" id="empty-msg">Aún no has añadido ninguna hipoteca para comparar.</p>';
        return;
    }

    mortgages.forEach((m, index) => {
        const card = document.createElement('div');
        card.className = 'mortgage-card';
        card.style.setProperty('--card-color', m.color);
        
        card.innerHTML = `
            <button class="delete-btn" onclick="removeMortgage(${m.id})" title="Eliminar">&times;</button>
            <div class="mortgage-title">Opción ${index + 1}</div>
            <div class="card-data">
                <div class="data-row">
                    <span class="data-label">Plazo:</span>
                    <span class="data-value">${m.params.plazoAnios} años, ${m.params.interesAnual}%</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Cuota:</span>
                    <span class="data-value highlight">${formatter.format(m.results.cuota_mensual)}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Intereses:</span>
                    <span class="data-value">${formatter.format(m.results.total_intereses)}</span>
                </div>
                <div class="data-row">
                    <span class="data-label">Total:</span>
                    <span class="data-value">${formatter.format(m.results.pago_total)}</span>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

function renderChart() {
    const ctx = document.getElementById('amortizationChart').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }

    if (mortgages.length === 0) {
        return; 
    }

    let maxYears = 0;
    mortgages.forEach(m => {
        if (m.params.plazoAnios > maxYears) {
            maxYears = m.params.plazoAnios;
        }
    });

    const labels = Array.from({length: maxYears + 1}, (_, i) => `Año ${i}`);

    const datasets = mortgages.map((m, idx) => {
        const data = Array(maxYears + 1).fill(0);
        m.results.amortizacion_anual.forEach(ay => {
            data[ay.year] = ay.balance;
        });
        
        return {
            label: `Opción ${idx + 1} (${m.params.plazoAnios}a, ${m.params.interesAnual}%)`,
            data: data,
            borderColor: m.color,
            backgroundColor: m.color,
            tension: 0.1,
            fill: false
        };
    });

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString('es-ES') + ' €';
                        },
                        color: '#94a3b8'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#f8fafc'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += formatter.format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}
