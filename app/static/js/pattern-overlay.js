class PatternOverlay {
    constructor(chart) {
        this.chart = chart;
        this.patterns = [];
        this.lines = [];
        this.shapes = [];
        this.labels = [];
    }

    clear() {
        // Xóa tất cả các line, shape và label hiện tại
        [...this.lines, ...this.shapes, ...this.labels].forEach(obj => {
            this.chart.removeEntity(obj);
        });
        this.lines = [];
        this.shapes = [];
        this.labels = [];
    }

    drawPatterns(patterns) {
        this.clear();
        this.patterns = patterns;

        patterns.forEach(pattern => {
            switch (pattern.pattern_type) {
                case 'head_and_shoulders':
                    this.drawHeadAndShoulders(pattern);
                    break;
                case 'double_top':
                    this.drawDoubleTop(pattern);
                    break;
                case 'double_bottom':
                    this.drawDoubleBottom(pattern);
                    break;
                case 'triple_top':
                    this.drawTripleTop(pattern);
                    break;
                case 'triple_bottom':
                    this.drawTripleBottom(pattern);
                    break;
                case 'symmetric_triangle':
                    this.drawSymmetricTriangle(pattern);
                    break;
                case 'ascending_triangle':
                    this.drawAscendingTriangle(pattern);
                    break;
                case 'descending_triangle':
                    this.drawDescendingTriangle(pattern);
                    break;
                case 'rising_wedge':
                    this.drawRisingWedge(pattern);
                    break;
                case 'falling_wedge':
                    this.drawFallingWedge(pattern);
                    break;
                case 'bull_flag':
                    this.drawBullFlag(pattern);
                    break;
                case 'bear_flag':
                    this.drawBearFlag(pattern);
                    break;
            }
        });
    }

    // Hàm vẽ các mô hình cụ thể
    drawHeadAndShoulders(pattern) {
        const color = pattern.confidence >= 0.8 ? '#f23645' : '#ffa500';
        const points = pattern.points || [];
        if (points.length < 5) return;

        // Vẽ các đỉnh vai-đầu-vai
        this.lines.push(this.chart.createShape(
            { time: points[0].time, price: points[0].price },
            { time: points[1].time, price: points[1].price },
            { color: color, width: 2 }
        ));
        this.lines.push(this.chart.createShape(
            { time: points[1].time, price: points[1].price },
            { time: points[2].time, price: points[2].price },
            { color: color, width: 2 }
        ));
        this.lines.push(this.chart.createShape(
            { time: points[2].time, price: points[2].price },
            { time: points[3].time, price: points[3].price },
            { color: color, width: 2 }
        ));
        this.lines.push(this.chart.createShape(
            { time: points[3].time, price: points[3].price },
            { time: points[4].time, price: points[4].price },
            { color: color, width: 2 }
        ));

        // Vẽ đường neckline
        this.lines.push(this.chart.createShape(
            { time: points[0].time, price: points[0].price },
            { time: points[4].time, price: points[4].price },
            { color: color, width: 2, style: 2 }
        ));

        // Thêm nhãn
        this.labels.push(this.chart.createShape(
            { time: points[2].time, price: points[2].price },
            { text: `H&S (${(pattern.confidence * 100).toFixed(1)}%)`, color: color }
        ));
    }

    drawDoubleTop(pattern) {
        const color = pattern.confidence >= 0.8 ? '#f23645' : '#ffa500';
        const points = pattern.points || [];
        if (points.length < 4) return;

        // Vẽ 2 đỉnh
        this.lines.push(this.chart.createShape(
            { time: points[0].time, price: points[0].price },
            { time: points[1].time, price: points[1].price },
            { color: color, width: 2 }
        ));
        this.lines.push(this.chart.createShape(
            { time: points[1].time, price: points[1].price },
            { time: points[2].time, price: points[2].price },
            { color: color, width: 2 }
        ));
        this.lines.push(this.chart.createShape(
            { time: points[2].time, price: points[2].price },
            { time: points[3].time, price: points[3].price },
            { color: color, width: 2 }
        ));

        // Vẽ đường neckline
        this.lines.push(this.chart.createShape(
            { time: points[0].time, price: points[0].price },
            { time: points[2].time, price: points[2].price },
            { color: color, width: 2, style: 2 }
        ));

        // Thêm nhãn
        this.labels.push(this.chart.createShape(
            { time: points[1].time, price: points[1].price },
            { text: `DT (${(pattern.confidence * 100).toFixed(1)}%)`, color: color }
        ));
    }

    // Tương tự implement các hàm vẽ cho các mô hình khác...
    drawDoubleBottom(pattern) {
        // Implement vẽ Double Bottom
    }

    drawTripleTop(pattern) {
        // Implement vẽ Triple Top
    }

    drawTripleBottom(pattern) {
        // Implement vẽ Triple Bottom
    }

    drawSymmetricTriangle(pattern) {
        // Implement vẽ Symmetric Triangle
    }

    drawAscendingTriangle(pattern) {
        // Implement vẽ Ascending Triangle
    }

    drawDescendingTriangle(pattern) {
        // Implement vẽ Descending Triangle
    }

    drawRisingWedge(pattern) {
        // Implement vẽ Rising Wedge
    }

    drawFallingWedge(pattern) {
        // Implement vẽ Falling Wedge
    }

    drawBullFlag(pattern) {
        // Implement vẽ Bull Flag
    }

    drawBearFlag(pattern) {
        // Implement vẽ Bear Flag
    }
}
