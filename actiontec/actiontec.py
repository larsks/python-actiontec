#!/usr/bin/python

import os
import sys
import optparse
import cStringIO as StringIO

import pexpect

class ActiontecException(Exception):
    pass

class LoginFailed(ActiontecException):
    pass

class BadCommand(ActiontecException):
    pass

class Actiontec (object):
    def __init__ (self,
            address = '192.168.1.1',
            username = 'admin',
            password = 'password',
            port = 23,
            telnet_path = 'telnet'):
        self.address = address
        self.username = username
        self.password = password
        self.port = int(port)
        self.telnet_path = telnet_path

        self.connect()

    def connect(self):
        self.spawn = pexpect.spawn('%s %s %d' % (
            self.telnet_path,
            self.address,
            self.port))
        self.spawn.expect('Username:')
        self.spawn.sendline(self.username)
        self.spawn.expect('Password:')
        self.spawn.sendline(self.password)
        if self.spawn.expect(['Router>', 'Username:']) == 1:
            raise LoginFailed(self.username)

    def run(self, command):
        out = StringIO.StringIO()
        self.spawn.logfile_read = out
        self.spawn.sendline(command)
        which = self.spawn.expect(['Router>', 'Bad command'])
        self.spawn.logfile_read = None

        if which == 1:
            raise BadCommand(command)

        return out.getvalue()

    def disconnect(self):
        self.spawn.close()
        self.spawn = None

    def interfaces(self):
        res = self.run('net ifconfig')

        iface = None
        interfaces = {}

        for line in res.split('\n'):
            if 'Device' in line:
                if iface:
                    interfaces[iface['name']] = iface
                iface = { 'name': line.split()[1] }
            if 'state=' in line:
                iface['state'] = line.split('=')[-1].strip()

        return interfaces

def parse_args():
    p = optparse.OptionParser()
    p.add_option('-H', '--host', '--address', default='192.168.1.1')
    p.add_option('-u', '--user', default='admin')
    p.add_option('-p', '--password', default='password')

    return p.parse_args()

def main():
    opts, args = parse_args()

    a = Actiontec(opts.host, opts.user, opts.password)
    text = a.run(' '.join(args))
    print text

if __name__ == '__main__':
    main()

