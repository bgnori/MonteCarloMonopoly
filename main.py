#!/usr/bin/env python

import sys





t = int(sys.args[1])

with file('result.txt', 'w') as f:
  r = Runner(1, t)
  r.run()
