from prometheus_client import start_http_server
import prometheus_client as prom
import random
import time

# Create a metric to track time spent and requests made.
counter = prom.Counter('python_my_counter', 'This is my counter')
gauge = prom.Gauge('python_my_gauge', 'This is my gauge')
histogram = prom.Histogram('python_my_histogram', 'This is my histogram')
summary = prom.Summary('python_my_summary', 'This is my summary')

# Decorate function with metric.
@summary.time()
def process_request(t):
    """A dummy function that takes some time."""
    print(t)
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8009)
    print ("http://localhost:8009")

    while True:
        counter.inc(random.random())
        gauge.set(random.random() * 15 - 5)
        histogram.observe(random.random() * 10)
        summary.observe(random.random() * 10)
        process_request(random.random() * 5)
        time.sleep(1)
