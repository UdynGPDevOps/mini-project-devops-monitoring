from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'Request latency (seconds)',
    ['method', 'endpoint']
)

@app.route('/')
@REQUEST_LATENCY.labels(method='GET', endpoint='/').time()
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=200).inc()
    return '''
    <html>
        <head>
            <title>Mini Project: DevOps Monitoring Demo</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f7f7f7;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 30px;
                    background-color: white;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    border-radius: 10px;
                }
                h1 {
                    color: #28a745;
                }
                ul {
                    line-height: 1.8;
                }
                footer {
                    margin-top: 30px;
                    font-size: 0.9em;
                    color: #666;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 DevOps Monitoring Mini Project</h1>
                <p>This project demonstrates real-time monitoring of a containerized Flask application using:</p>
                <ul>
                    <li>Docker for app containerization</li>
                    <li>Prometheus for metrics collection</li>
                    <li>Grafana for dashboard visualization</li>
                    <li>Kubernetes for container orchestration</li>
                </ul>
                <p>🔍 Metrics are exposed at <a href="/metrics" target="_blank">/metrics</a> and scraped by Prometheus.</p>
                <p>💡 This project is part of my DevOps internship at Medtronic.</p>
                <footer>Made by Udayan Gupta</footer>
            </div>
        </body>
    </html>
    '''

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.errorhandler(404)
def not_found(e):
    REQUEST_COUNT.labels(method=request.method, endpoint='unknown', http_status=404).inc()
    return "404 - Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
