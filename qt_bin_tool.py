#!/usr/bin/env python
#
# qt_bin_tool.py {uic|rcc|moc} ...
#
# This script takes the header files and uses the Qt MOC to generate the Meta-Object source.
# The output files will be named: {header file name}.moc.cc
#
# Copyright (c) David Chen, 2017

import argparse
import os
import os.path
import subprocess
import sys, platform

# From https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def StripHeaderExtension(filename):
    if not filename.endswith(".h"):
        raise RuntimeError("Invalid header extension: "
                           "{0} .".format(filename))
    return filename.rsplit(".", 1)[0]


def main(argv):
    assert len(argv)>2, "not enough argv"
    assert argv[1] in ['rcc','uic','moc'], "not valid qt bin tool"

    # If QTDIR is in the environment, prefer using QTDIR so prepend to PATH.
    if 'QTDIR' in os.environ:
        os.environ['PATH'] = os.path.join(os.environ['QTDIR'], 'bin') \
                + os.pathsep + os.environ['PATH']
    
    # check wheather tool exists in the PATH
    if platform.system() == 'Windows':
        fullpath = which(argv[1]+'.exe')
    else:
        fullpath = which(argv[1])
    assert fullpath
    
    cmd = []
    ret = subprocess.call(argv[1:])
    if ret != 0:
        print(argv[1:])
        raise RuntimeError("Moc has returned non-zero status: "
                            "{0} .".format(ret))


if __name__ == "__main__":
    try:
        main(sys.argv)
    except RuntimeError as e:
        sys.exit(1)
