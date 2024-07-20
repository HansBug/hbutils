import os.path
import shutil

_GIT_LFS = shutil.which('git_lfs', path=os.path.abspath('dist'))
_GIT_RAW = shutil.which('git_raw', path=os.path.abspath('dist'))
