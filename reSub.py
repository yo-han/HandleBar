""" HandleBar """

import sys, os

sys.stdout.flush()
sys.stderr.flush()
so = file('/tmp/handleBarOut.log', 'a+')
se = file('/tmp/handleBarError.log', 'a+', 0)
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())

from app import *
from lib import *

reSub()