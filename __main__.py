from minimiser_api.app import app, min
import argparse
from cache.cache import Cache
import threading

def cache():
    cache = Cache(60*30)  # Update cache every 30 mins
    cache.start_caching()

def main(port):
    app.run(host='0.0.0.0', port=port)

parser = argparse.ArgumentParser()
parser.add_argument('-c', action='store_true')
parser.add_argument('-p')
args = parser.parse_args()

if args.c:
    min.set_cache(True)
    thread = threading.Thread(target=cache, daemon=True)
    thread.start()
else:
    min.set_cache(False)
if args.p:
    port = int(args.p)
else:
    port = 8080

main(port)
