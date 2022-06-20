from .main import windows
from .main import linux
import platform

if(platform.system() == 'Windows'):
    __ALL__ = [windows]
else:
    __ALL__ = [linux]
