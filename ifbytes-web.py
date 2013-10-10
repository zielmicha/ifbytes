#!/usr/bin/env python
from flask import Flask, Response, abort, request
import os
import json
app = Flask(__name__)

logdir = os.environ.get('LOGS', 'logs')

@app.route("/get/<dataset>")
def get_dataset(dataset):
    logfile, iface, tx = dataset.split(':')
    logfile += '.log'
    tx_i = 1 if (tx == 'tx') else 0
    if logfile in os.listdir(logdir):
        log = read_log(open(logdir + '/' + logfile))
        result = [ [time, ifaces[iface][tx_i]] for time, ifaces in log ]
        result = [ (time*1000, data) for time, data in derivate(result) ]
        return Response('%s' % (
            json.dumps(result)), content_type='application/json')
    else:
        raise Exception('not found')

def read_log(f):
    for line in f:
        data = line.split()
        time = float(data[0])
        values = [ seg.split(',') for seg in data[1:] ]
        ifaces = { seg[0]:(int(seg[1]), int(seg[2])) for seg in values }
        yield (time, ifaces)

def derivate(data):
    for (t0, a0), (t1, a1) in zip(data, data[1:]):
        if t0 == t1:
            continue
        yield (t0, (a0 - a1) / float(t0 - t1))

@app.route("/<name>")
def static(name):
    if name in ('viewer.js', 'viewer.html'):
        return open(name).read()
    else:
        abort(404)

if __name__ == "__main__":
    app.run()
