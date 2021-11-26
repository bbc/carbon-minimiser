from minimiser_api.app import app
import argparse
from cache.cache import Cache

def main(port):
    Cache(60*30)  # Update cache every 30 mins
    app.run(host='0.0.0.0', port=port)


parser = argparse.ArgumentParser()
parser.add_argument('-p')
args = parser.parse_args()
if args.p:
    port = int(args.p)
else:
    port = 8080

main(port)
