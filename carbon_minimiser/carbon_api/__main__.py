from carbon_intensity_exporter.exporter.prometheus import Prometheus
from prometheus_client import start_http_server
import time
from prometheus_client.core import REGISTRY
import argparse


def main(port):
    start_http_server(port)
    REGISTRY.register(Prometheus())
    while True:
        time.sleep(10)


parser = argparse.ArgumentParser()
parser.add_argument('-p')
args = parser.parse_args()
if args.p:
    port = int(args.p)
else:
    port = 8000

main(port)
