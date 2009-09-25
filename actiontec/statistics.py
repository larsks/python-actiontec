#!/usr/bin/python

import actiontec

IFSTAT_FIELDS = '''
    rx_bytes rx_packets rx_errs rx_drop rx_fifo rx_frame rx_compressed rx_multicast'
    tx_bytes tx_packets tx_errs tx_drop tx_fifo tx_colls tx_carrier tx_compressed
    '''.split()

class Statistics (actiontec.Actiontec):
    def ifstats(self):
        res = self.run('system cat /proc/net/dev')

        devices = {}
        for line in res.split('\n'):
            if ':' in line:
                iface, stats = [x.strip() for x in line.split(':')]
                devices[iface] = dict(zip(IFSTAT_FIELDS,
                    [int(x) for x in stats.split()]))

        return devices

    def loadavg(self):
        res = self.run('kernel cpu_load_avg')
        state = 0

        for line in res.split('\n'):
            if state == 0:
                if line.startswith('1 Min.'):
                    state = 1
            elif state == 1:
                loadavg = line.split()
                break

        return [float(x) for x in loadavg]

    def meminfo(self):
        res = self.run('kernel meminfo')
        meminfo = {}

        for line in res.split('\n'):
            if line.startswith('Memory info:'):
                pass
            elif ':' in line:
                k = line.split(':')[0]
                v = line.split(':')[1].split()[0]
                meminfo[k] = int(v)

        return meminfo

    def processes(self):
        res = self.run('kernel top')
        state = 0
        processes = []

        for line in res.split('\n'):
            if state == 0:
                if line.startswith('Command'):
                    state = 1
            elif state == 1:
                if line.startswith('Wireless Broadband'):
                    break
                else:
                    processes.append(line.split()[0])

        return processes

    def cpus(self):
        res = self.run('system cat /proc/cpuinfo')

        cpus = []
        cpu = {}
        for line in res.split('\n'):
            if not ':' in line:
                continue
            elif ':' in line:
                k,v = [x.strip() for x in line.split(':')]
                if k == 'system type':
                    continue
                elif k == 'processor' and cpu:
                    cpus.append(cpu)
                    cpu = {}

                cpu[k] = v

        if cpu:
            cpus.append(cpu)

        return cpus

