import argparse
from app import app

parser = argparse.ArgumentParser(description='PT-TestTask')
parser.add_argument('--host',       type=str, default='127.0.0.1',  help='Host url for UI')
parser.add_argument('--port',       type=str, default='5000',       help='Port for UI')
parser.add_argument('--dbendpoint', type=str, default='http://192.168.1.20:9999/blazegraph/namespace/kb/sparql',           help='SPARQL endpoint address')
parser.add_argument('--debug',      type=bool,default=False)
args = parser.parse_args()
app.dbendpoint = args.dbendpoint
app.run(host=args.host, port=args.port, debug = args.debug)