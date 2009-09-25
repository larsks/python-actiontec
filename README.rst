=================================================
Python utilities for the Actiontec MI424WR Router
=================================================

:Author: Lars Kellogg-Stedman
:URL: http://github.com/larsks/python-actiontec

Overview
========

This is a Python API for interacting with the Actiontec MI424WR
router, as used by Verizon's FIOS service.  The package includes the
following classes:

- actiontec.actiontec.Actiontec

  This is a very thin wrapper around the pexpect_ project that lets
  you send commands to the Actiontec router via the telnet interface
  and receive back the result text.

- actiontec.statistics.Statistics

  This class extends the Actiontec class to include convenience
  functions for retrieving common operating statistics from the
  Actiontec router.

Requirements
============

- You need to enable the telnet administration interface on your
  router.

  - Log in to your router.

  - Select "Advanced".

  - "Yes", you want to proceed.

  - Select "Local Administration", located in the menu under the
    toolbox icon.

  - Under "Allow local telnet access", enable "Using Primary Telnet
    port (23)".

  - Click "Apply".

- You need the ``telnet`` command.  If you're on Linux or OS X you're
  probably in good shape.

- You will need to install pexpect_.

  - If you are on CentOS::

    # yum install pexpect

  - If you are on Ubuntu::

    # apt-get install python-pexpect

  - If you are on something else and you have the ``setuptools`` package
    installed::

    # easy_install pexpect

**NB**: It's possible that the pexpect_ module will only run on
Unix-like platforms (Linux, OS X, (Free|Net|Open|)BSD, etc).

Examples
========

Following are some simple examples.  See the inline documentation
(``pydoc actiontec``) for additional API details.

Basic usage
-----------

The following code prints out the top level help output::

  from actiontec.actiontec import Actiontec

  a = Actiontec()
  text = a.run('help')

This assumes you are using the default password ("password").  If you
have changed your password, the code would look like this::

  a = Actiontec(password='mypassword')

If you provide invalid credentials for logging in, the code will raise
``actiontec.actiontec.LoginFailed``.  If you try to run an invalid
command, the code will raise ``actiontec.actiontec.BadCommand``.

Getting statistics
------------------

If you would like to retrieve the 1, 5, and 15 minute load average
from your router, you would run code similar to the following::

  from actiontec.statistics import Statistics

  a = Statistics()
  avg1, avg5, avg15 = a.loadavg()

To get detailed interface statistics::

  stats = a.ifstats()

The ``ifstats`` method returns a dictionary of which the keys are
interface names and the following parameters extracted from
``/proc/net/dev``:

- rx_bytes
- rx_packets
- rx_errs
- rx_drop
- rx_fifo
- rx_frame
- rx_compressed
- rx_multicast'
- tx_bytes
- tx_packets
- tx_errs
- tx_drop
- tx_fifo
- tx_colls
- tx_carrier
- tx_compressed

Security considerations
=======================

This code uses telnet to interact with your router.  This means that
the username and password are sent over your network in cleartext.
This has security implications, especially in a wireless environment:
it is possible that with an appropriate level of access someone would
be able to acquire your credentials and then have administrative
access to your router.

You have several options for responding to this information:

#. You can ignore it.  You're the best judge of the particular
   security risks associated with your own network.

#. You can use an SSL-enabled telnet client.

   While the router support SSL-encrypted telnet, the telnet client
   distributed with most operating systems does not include SSL
   support.  You may need to build your own version with SSL support. 

   You will need to specify an alternate port when using this
   API if you pursue this solution.

#. You can use an SSL wrapper.

   Programs such as stunnel_ can be used to provide SSL support to
   tools that otherwise would communicate over a cleartext connection.
   You would use stunnel_ to forward a local port on your computer to
   the SSL telnet port on the router.

   You will need to specify an alternate port when using this
   API if you pursue this solution.

.. _pexpect: http://pexpect.sourceforge.net/pexpect.html
.. _stunnel: http://www.stunnel.org/

