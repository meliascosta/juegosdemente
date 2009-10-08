import sys
import zipfile
import os
import os.path
import getopt

def unzip(zf, dir):
    def _makedirs(directories, basedir):
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs():
        dirs = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)
        dirs.sort()
        return dirs
    
    def _createstructure(dir):
        _makedirs(_listdirs(), dir)
    
    if not dir.endswith(':') and not os.path.exists(dir):
        os.mkdir(dir)

    _createstructure(dir)

    for i, name in enumerate(zf.namelist()):
        if not name.endswith('/'):
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zf.read(name))
            outfile.flush()
            outfile.close()
