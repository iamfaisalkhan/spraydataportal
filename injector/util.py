import zipfile
import tarfile
import os
from hurry.filesize import size

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip"% (dst), "w", zipfile.ZIP_DEFLATED)
    for afile in src:
        absname = os.path.abspath(afile)
        arcname = "%s/%s"%(dst, os.path.basename(afile))
        print "zipping %s as %s" % (afile, arcname)
        zf.write(absname, arcname)

    zf.close()

def tar(src, dst):
    tar = tarfile.open("%s.tar.gz"%(dst), "w:gz")

    for afile in src:
        absname = os.path.abspath(afile)
        arcname = "%s/%s"%(dst, os.path.basename(afile))
        print "tar.gz %s as %s" % (afile, arcname)
        tar.add(absname, arcname)

    tar.close()


def fileInfo(files):
    info = {}
    for file in files:
        info[file] = {}
        info[file]['name'] = os.path.basename(file)
        stats = os.stat(file)
        info[file]['size'] = size(stats.st_size)

    return info