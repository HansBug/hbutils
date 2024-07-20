import glob
import os.path

_GIT_LFSS = glob.glob(os.path.join('dist', 'git_lfs*'))
_GIT_LFS = _GIT_LFSS[0] if _GIT_LFSS else None

_GIT_RAWS = glob.glob(os.path.join('dist', 'git_raw*'))
_GIT_RAW = _GIT_RAWS[0] if _GIT_RAWS else None
