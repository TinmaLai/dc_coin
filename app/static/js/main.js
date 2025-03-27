// Theme management
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;
let isDarkMode = true;

themeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    updateTheme();
});

function updateTheme() {
    if (isDarkMode) {
        body.classList.add('bg-dark');
        body.classList.add('text-light');
        themeToggle.innerHTML = '<i class="bi bi-moon-stars"></i>';
    } else {
        body.classList.remove('bg-dark');
        body.classList.remove('text-light');
        themeToggle.innerHTML = '<i class="bi bi-sun"></i>';
    }
}

// Pagination management
let currentPage = 1;
const itemsPerPage = 10;
let allPatterns = [];
let stats = {};

// Format date to local Vietnamese time
function formatDate(dateString) {
    const options = {
        timeZone: 'Asia/Ho_Chi_Minh',
        hour12: false,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleString('vi-VN', options);
}

// Format number with thousand separators
function formatNumber(number) {
    return new Intl.NumberFormat('vi-VN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 8
    }).format(number);
}

// Get confidence level class and icon
function getConfidenceDisplay(confidence) {
    let cls, icon;
    if (confidence >= 0.8) {
        cls = 'confidence-high';
        icon = 'bi-check-circle-fill';
    } else if (confidence >= 0.6) {
        cls = 'confidence-medium';
        icon = 'bi-exclamation-circle-fill';
    } else {
        cls = 'confidence-low';
        icon = 'bi-question-circle-fill';
    }
    return {
        class: cls,
        icon: icon
    };
}

// Create table row for a pattern
function createPatternRow(pattern) {
    const row = document.createElement('tr');
    row.className = 'new-pattern';
    const confidence = getConfidenceDisplay(pattern.confidence);
    
    row.innerHTML = `
        <td>${formatDate(pattern.timestamp)}</td>
        <td>
            <strong class="text-warning">${pattern.symbol}</strong>
        </td>
        <td>
            <span class="badge bg-warning text-dark">
                ${pattern.pattern_type.replace('_', ' ').toUpperCase()}
            </span>
        </td>
        <td>${formatNumber(pattern.price)} USDT</td>
        <td class="${confidence.class}">
            <i class="bi ${confidence.icon} me-1"></i>
            ${(pattern.confidence * 100).toFixed(1)}%
        </td>
        <td>${pattern.description}</td>
    `;
    return row;
}

// Create pagination controls
function createPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';
    
    // Previous button
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `
        <a class="page-link" href="#" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
        </a>
    `;
    prevLi.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            displayPatterns();
        }
    });
    pagination.appendChild(prevLi);
    
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === currentPage ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
        li.addEventListener('click', () => {
            currentPage = i;
            displayPatterns();
        });
        pagination.appendChild(li);
    }
    
    // Next button
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `
        <a class="page-link" href="#" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
        </a>
    `;
    nextLi.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            displayPatterns();
        }
    });
    pagination.appendChild(nextLi);
}

// Filter patterns based on search and filter criteria
function filterPatterns() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const patternFilter = document.getElementById('pattern-filter').value;
    
    return allPatterns.filter(pattern => {
        const matchesSearch = pattern.symbol.toLowerCase().includes(searchTerm) ||
                            pattern.description.toLowerCase().includes(searchTerm);
        const matchesFilter = !patternFilter || pattern.pattern_type === patternFilter;
        return matchesSearch && matchesFilter;
    });
}

// Display patterns with pagination
function displayPatterns() {
    const filteredPatterns = filterPatterns();
    const start = (currentPage - 1) * itemsPerPage;
    const paginatedPatterns = filteredPatterns.slice(start, start + itemsPerPage);
    
    const tableBody = document.getElementById('patterns-table');
    tableBody.innerHTML = '';
    
    paginatedPatterns.forEach(pattern => {
        tableBody.appendChild(createPatternRow(pattern));
    });
    
    createPagination(filteredPatterns.length);
    updateDashboardStats();
}

// Update dashboard stats
function updateDashboardStats() {
    if (stats) {
        document.querySelector('.total-patterns').textContent = stats.total_patterns || 0;
        document.querySelector('.recent-patterns').textContent = stats.recent_patterns || 0;
        document.querySelector('.active-coins').textContent = stats.active_coins || 0;
        document.querySelector('.accuracy-rate').textContent = 
            `${((stats.accuracy_rate || 0) * 100).toFixed(1)}%`;
        
        updateCharts(allPatterns);
    }
}

// Initialize and update charts
function updateCharts(patterns) {
    if (!patterns || patterns.length === 0) return;

    // Pattern distribution chart
    const patternCounts = patterns.reduce((acc, p) => {
        acc[p.pattern_type] = (acc[p.pattern_type] || 0) + 1;
        return acc;
    }, {});
    
    const distributionOptions = {
        series: [{
            data: Object.values(patternCounts)
        }],
        chart: {
            type: 'bar',
            height: 300,
            background: 'transparent',
            foreColor: '#fff'
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: false,
            }
        },
        xaxis: {
            categories: Object.keys(patternCounts).map(k => k.replace('_', ' ').toUpperCase())
        },
        theme: {
            mode: 'dark'
        },
        colors: ['#ffd700']
    };
    
    if (!window.distributionChart) {
        window.distributionChart = new ApexCharts(
            document.querySelector("#patterns-distribution-chart"), 
            distributionOptions
        );
        window.distributionChart.render();
    } else {
        window.distributionChart.updateOptions(distributionOptions);
    }
    
    // Top coins chart
    const coinCounts = patterns.reduce((acc, p) => {
        acc[p.symbol] = (acc[p.symbol] || 0) + 1;
        return acc;
    }, {});
    
    const sortedCoins = Object.entries(coinCounts)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 5);
    
    const topCoinsOptions = {
        series: sortedCoins.map(([,count]) => count),
        chart: {
            type: 'donut',
            height: 300,
            background: 'transparent'
        },
        labels: sortedCoins.map(([symbol]) => symbol),
        theme: {
            mode: 'dark'
        },
        colors: ['#ffd700', '#ffa500', '#ff8c00', '#ff7f50', '#ff6347'],
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 200
                },
                legend: {
                    position: 'bottom'
                }
            }
        }]
    };
    
    if (!window.topCoinsChart) {
        window.topCoinsChart = new ApexCharts(
            document.querySelector("#top-coins-chart"), 
            topCoinsOptions
        );
        window.topCoinsChart.render();
    } else {
        window.topCoinsChart.updateOptions(topCoinsOptions);
    }
}

// Setup event listeners
document.getElementById('search-input').addEventListener('input', () => {
    currentPage = 1;
    displayPatterns();
});

document.getElementById('pattern-filter').addEventListener('change', () => {
    currentPage = 1;
    displayPatterns();
});

// Fetch and update data
function updateData() {
    fetch('/api/patterns')
        .then(response => response.json())
        .then(data => {
            allPatterns = data.patterns;
            stats = data.stats;
            displayPatterns();
        })
        .catch(error => console.error('Error fetching patterns:', error));
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    updateData();
    // Refresh data every minute
    setInterval(updateData, 60000);
});
