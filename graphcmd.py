#!/usr/bin/env python


import re

cpat = re.compile(r"^class (?P<name>.+)\((?:model\.)?Command\):")
used = re.compile(r"[A-Z][a-z]+[A-Z][A-Za-z]+")

result = {}

def foo(d, f):
  found = ''
  for line in f.readlines():
    for found in cpat.findall(line):
      v = d.get(found, None)
      if v is None:
        v = set()
      d[found] = v
    if found and line.startswith(' '*4):
      for appear in used.findall(line):
        d[found].add(appear)
  return d

with file('/home/nori/Desktop/work/SurveyOnMonopoly/command.py') as f:
  result = foo(result, f)

with file('/home/nori/Desktop/work/SurveyOnMonopoly/model.py') as f:
  result = foo(result, f)



print "digraph evoke {"
for k, v in result.iteritems():
  for dst in v:
    print k, '->', dst, ';'
  if len(v) == 0:
    print k, '-> none ;'

print "}"


