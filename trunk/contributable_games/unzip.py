import sys
import zipfile
import os
import os.path
import getopt

def unzip(zf, dir):
    for i, name in enumerate(zf.namelist()):
        if not name.endswith('/'):
            dirname = os.path.dirname(os.path.join(dir, name))
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            outfile = open(os.path.join(dir, name), 'wb')
            outfile.write(zf.read(name))
            outfile.flush()
            outfile.close()
