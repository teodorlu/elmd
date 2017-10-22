#!/usr/bin/python

from __future__ import print_function

import subprocess
import os
import fileinput
import re


is_src = re.compile(r"^&\selmd\ssrc").match
is_app = re.compile(r"^&\selmd\sapp").match


def slurp(path):
    with open(path, "r") as f:
        return f.read()


def src(line):
    words = line.split()
    if len(words) < 4:
        return "Expecting source file after 'src': " + line
    sourcefile = words[3]
    return """```elm
{}
```""".format(slurp(sourcefile))


def app(line):
    words = line.split()
    if len(words) < 4:
        return "Expecting source file after 'app'" + line
    sourcefile = words[3]
    targetfile = sourcefile + ".html"

    # Shell out to compile the elm file
    FNULL = open(os.devnull, 'w')
    subprocess.call(
        ["elm", "make", sourcefile, "--output", targetfile],
        stdout=FNULL,
        stderr=subprocess.STDOUT)
    return words # "app:" + line


def process_line(line):
    if is_src(line):
        return src(line)
    elif is_app(line):
        return app(line)
    else:
        return line


things = fileinput.input()
for line in things:
    print(process_line(line) + "", end='')
