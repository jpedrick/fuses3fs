import os, stat, errno, sys
from xdg import(XDG_CONFIG_HOME)
from importlib.machinery import SourceFileLoader

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/libs/')
config_path = os.environ.get('FUSES3FS_CONFIG', str(XDG_CONFIG_HOME) + '/fuses3fsrc/config.py') 

settings = SourceFileLoader('config', config_path ).load_module().settings()

try:
    import _find_fuse_parts
except ImportError:
    pass

import fuse
from fuse import Fuse

class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode  = 0
        self.st_ino   = 0
        self.st_dev   = 0
        self.st_nlink = 0
        self.st_uid   = 0
        self.st_gid   = 0
        self.st_size  = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class FuseS3FS(Fuse):
    def __init__(self):
        import boto3
        self.s3 = boto3.client('s3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key
             )
