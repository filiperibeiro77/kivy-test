#!/usr/bin/env python

from os import path
import subprocess
import sys

main = path.join(path.dirname(path.abspath(path.realpath(__file__))), "main.py")
proc = subprocess.Popen(["python", main] + sys.argv[1:])
proc.wait()
sys.exit(proc.poll())


