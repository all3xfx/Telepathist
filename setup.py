import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable('Telepathist.py', base=base)]

setup(name='Telepathist',version='0.1',description='Artificial Intelligence Project',executables=executables)