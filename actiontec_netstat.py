#!/usr/bin/python

import os
import sys
import optparse
import pprint

import actiontec

NETSTAT_FIELDS = '''
    rx_bytes rx_packets rx_errs rx_drop rx_fifo rx_frame rx_compressed rx_multicast'
    tx_bytes tx_packets tx_errs tx_drop tx_fifo tx_colls tx_carrier tx_compressed
    '''.split()

Router = None

def stripped(fd):
    for line in fd:
        yield line.strip()

def enumerate_interfaces():
    global Router
    res = Router.run('net ifconfig')

    dev = None
    devices = []

    for line in res.split('\n'):
        if 'Device' in line:
            if dev:
                devices.append(dev)

            dev = { 'name': line.split()[1] }
        if 'state=' in line:
            dev['state'] = line.split('=')[-1].strip()

    return devices

def metric_update ():
    pass

def make_descriptors(params, name):
    if 'values' in params:
        values = params['values'].split()
    else:
        values = NETSTAT_FIELDS

    descriptors = []
    for v in values:
        descriptors.append({
            'name': '%s_%s' % (name, v),
            'call_back': metric_update,
            'time_max': 90,
            'value_type': 'uint',
            'slope': 'both',
            'format': '%u',
            'groups': 'network'
            })
        
    return descriptors

def metric_init(params):
    global Router

    Router = actiontec.Actiontec(
            address = params.get('address', '192.168.1.1'),
            username = params.get('username', 'admin'),
            password = params.get('password', 'password')
            )

    
    interfaces = enumerate_interfaces()
    descriptors = []

    for iface in interfaces:
        if iface['state'] == 'running':
            descriptors.extend(make_descriptors(params, iface['name']))

    return descriptors

if __name__ == '__main__':
    pprint.pprint(metric_init({
        'password': 'nutsh3ll',
        'values': 'rx_bytes rx_errs rx_packets rx_drop tx_bytes tx_packets tx_errors tx_drop'
        }))
