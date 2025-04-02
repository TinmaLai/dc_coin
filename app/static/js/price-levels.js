class PriceLevels {
    constructor(chart) {
        this.chart = chart;
        this.visible = true;
        this.lines = {
            entry: null,
            stopLoss: null,
            takeProfit: null
        };
        this.labels = {
            entry: null,
            stopLoss: null,
            takeProfit: null
        };
        this.levels = {
            entry: 0,
            stopLoss: 0,
            takeProfit: 0
        };
        this.isDragging = false;
        this.currentLabel = null;

        // Bind event handlers
        this.onMouseDown = this.onMouseDown.bind(this);
        this.onMouseMove = this.onMouseMove.bind(this);
        this.onMouseUp = this.onMouseUp.bind(this);

        // Setup event listeners
        this.chart.subscribeClick(this.onMouseDown);
        document.addEventListener('mousemove', this.onMouseMove);
        document.addEventListener('mouseup', this.onMouseUp);
    }

    setLevels(entry, stopLoss, takeProfit) {
        this.levels = {
            entry: entry,
            stopLoss: stopLoss,
            takeProfit: takeProfit
        };
        this.draw();
    }

    show() {
        this.visible = true;
        this.draw();
    }

    hide() {
        this.visible = false;
        this.clear();
    }

    clear() {
        // Remove all lines and labels
        Object.values(this.lines).forEach(line => {
            if (line) {
                this.chart.removeEntity(line);
            }
        });
        Object.values(this.labels).forEach(label => {
            if (label) {
                this.chart.removeEntity(label);
            }
        });

        this.lines = {
            entry: null,
            stopLoss: null,
            takeProfit: null
        };
        this.labels = {
            entry: null,
            stopLoss: null,
            takeProfit: null
        };
    }

    draw() {
        if (!this.visible) return;
        this.clear();

        const currentPrice = this.chart.getLastClose();
        const time = this.chart.getLastTime();

        // Entry line
        if (this.levels.entry) {
            this.lines.entry = this.chart.createShape(
                { price: this.levels.entry, time: time },
                { color: '#ffd700', width: 2, style: 1 }
            );
            this.labels.entry = this.chart.createLabel(
                { price: this.levels.entry, time: time },
                { text: `Entry: ${this.levels.entry.toFixed(2)}`, color: '#ffd700' }
            );
        }

        // Stop Loss line
        if (this.levels.stopLoss) {
            this.lines.stopLoss = this.chart.createShape(
                { price: this.levels.stopLoss, time: time },
                { color: '#f23645', width: 2, style: 1 }
            );
            this.labels.stopLoss = this.chart.createLabel(
                { price: this.levels.stopLoss, time: time },
                { text: `SL: ${this.levels.stopLoss.toFixed(2)}`, color: '#f23645' }
            );
        }

        // Take Profit line
        if (this.levels.takeProfit) {
            this.lines.takeProfit = this.chart.createShape(
                { price: this.levels.takeProfit, time: time },
                { color: '#089981', width: 2, style: 1 }
            );
            this.labels.takeProfit = this.chart.createLabel(
                { price: this.levels.takeProfit, time: time },
                { text: `TP: ${this.levels.takeProfit.toFixed(2)}`, color: '#089981' }
            );
        }

        this.updateRiskRewardRatio();
    }

    updateRiskRewardRatio() {
        if (!this.levels.entry || !this.levels.stopLoss || !this.levels.takeProfit) return;

        const risk = Math.abs(this.levels.entry - this.levels.stopLoss);
        const reward = Math.abs(this.levels.entry - this.levels.takeProfit);
        const ratio = (reward / risk).toFixed(2);
        const direction = this.levels.takeProfit > this.levels.entry ? 'LONG' : 'SHORT';

        // Hiển thị thông tin R/R
        const container = document.createElement('div');
        container.className = 'price-levels-info';
        container.innerHTML = `
            <div class="d-flex justify-content-between align-items-center bg-dark p-2 border border-warning rounded">
                <div>
                    <span class="badge ${direction === 'LONG' ? 'bg-success' : 'bg-danger'}">${direction}</span>
                </div>
                <div class="text-warning">
                    R/R: 1:${ratio}
                </div>
                <div>
                    <button class="btn btn-sm btn-outline-warning" onclick="sendTelegramAlert()">
                        <i class="bi bi-telegram"></i> Alert
                    </button>
                </div>
            </div>
        `;

        // Thêm container vào chart
        const chartContainer = document.getElementById('tv_chart_container');
        const existingInfo = chartContainer.querySelector('.price-levels-info');
        if (existingInfo) {
            existingInfo.remove();
        }
        chartContainer.appendChild(container);
    }

    onMouseDown(param) {
        if (!this.visible) return;

        const price = param.price;
        const time = param.time;

        // Kiểm tra nếu click gần một trong các line
        if (this.isNearLine(price, this.levels.entry)) {
            this.isDragging = true;
            this.currentLabel = 'entry';
        } else if (this.isNearLine(price, this.levels.stopLoss)) {
            this.isDragging = true;
            this.currentLabel = 'stopLoss';
        } else if (this.isNearLine(price, this.levels.takeProfit)) {
            this.isDragging = true;
            this.currentLabel = 'takeProfit';
        }
    }

    onMouseMove(event) {
        if (!this.isDragging || !this.currentLabel) return;

        const price = this.chart.coordsToPrice(event.clientY);
        this.levels[this.currentLabel] = price;
        this.draw();
    }

    onMouseUp() {
        this.isDragging = false;
        this.currentLabel = null;
    }

    isNearLine(price1, price2, threshold = 0.001) {
        return Math.abs(price1 - price2) / price2 < threshold;
    }

    cleanup() {
        // Remove event listeners
        document.removeEventListener('mousemove', this.onMouseMove);
        document.removeEventListener('mouseup', this.onMouseUp);
        this.chart.unsubscribeClick(this.onMouseDown);
    }
}

// Hàm gửi cảnh báo telegram
async function sendTelegramAlert() {
    try {
        const response = await fetch('/api/send-alert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol: tvChart.symbol,
                entry: priceLevels.levels.entry,
                stopLoss: priceLevels.levels.stopLoss,
                takeProfit: priceLevels.levels.takeProfit
            })
        });
        
        const data = await response.json();
        if (data.success) {
            alert('Đã gửi cảnh báo thành công!');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        alert('Lỗi khi gửi cảnh báo: ' + error.message);
    }
}
