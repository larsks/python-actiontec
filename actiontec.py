#!/usr/bin/python2.6

import os
import sys
import optparse
import cStringIO as StringIO

import pexpect

class Actiontec (object):
    def __init__ (self, address = '192.168.1.1', username = 'admin',
            password = 'password'):
        self.address = address
        self.username = username
        self.password = password

        self.connect()

    def connect(self):
        self.spawn = pexpect.spawn('telnet %s' % self.address)
        self.spawn.expect('Username:')
        self.spawn.sendline(self.username)
        self.spawn.expect('Password:')
        self.spawn.sendline(self.password)
        self.spawn.expect('Router>')

    def run(self, command):
        out = StringIO.StringIO()
        self.spawn.logfile_read = out
        self.spawn.sendline(command)
        self.spawn.expect('Router>')
        self.spawn.logfile_read = None

        return out.getvalue()

    def disconnect(self):
        self.spawn.close()
        self.spawn = None

def main():
    a = Actiontec('192.168.1.1', 'admin', 'nutsh3ll')
    text = a.run(' '.join(sys.argv[1:]))
    print text

if __name__ == '__main__':
    main()

