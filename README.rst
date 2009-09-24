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

If you would like to retrieve the 1, 5, and 10 minute load average
from your router, you would run code similar to the following::

  from actiontec.statistics import Statistics

  a = Statistics()
  avg1, avg5, avg10 = a.loadavg()

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

.. _pexpect: http://pexpect.sourceforge.net/pexpect.html

