from carbon_minimiser.api.app import app
import argparse


def main(port):
    app.run(host='0.0.0.0', port=port)


parser = argparse.ArgumentParser()
parser.add_argument('-p')
args = parser.parse_args()
if args.p:
    port = int(args.p)
else:
    port = 8080

main(port)
