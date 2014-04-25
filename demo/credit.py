#!/usr/bin/python

from agi import *
from db import *
import sys
import time
import string
import math

if __name__ == '__main__':

    callerid = str(sys.argv[1]).strip()
    ag       = AGI()
    data     = db()

    credit = data.get_credit(callerid)
    data.discount(callerid)
    ag.set_variable('CREDIT', int(credit))
    sys.exit(0)

