#!/usr/bin/python

import os
import sys
import optparse

from actiontec.statistics import Statistics

def parse_args():
    p = optparse.OptionParser()
    p.add_option('-H', '--host', '--address', default='192.168.1.1')
    p.add_option('-u', '--user', default='admin')
    p.add_option('-p', '--password', default='password')
    p.add_option('-a', '--all', action='store_true')

    return p.parse_args()

def main():
    opts, args = parse_args()

    a = Statistics(opts.host, opts.user, opts.password)
    
    ifaces = a.interfaces()
    print ifaces

    for iface, stats in a.ifstats().items():
        try:
            if (not opts.all) and ifaces[iface]['state'] not in ['running']:
                continue
        except KeyError:
            if not opts.all:
                continue

        print iface
        for k,v in stats.items():
                print '%20s = %s' % (k,v)

if __name__ == '__main__':
    main()

