#!/usr/bin/env python

import sys

import pypoly.montecarlo



t = int(sys.argv[1])

with file('result.txt', 'w') as f:
  r = pypoly.montecarlo.Runner(1, f)
  r.run()
