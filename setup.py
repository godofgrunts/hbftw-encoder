from cx_Freeze import setup, Executable

includefiles = ['handbrake\\', 're.py', 'sre_compile.py', 'sre_constants.py', 'sre_parse.py']
includes = ['os', 'time', 'subprocess']

setup(
    name = 'Handbrake for the win Encoder',
    version = '0.4',
    description = 'Unoffical AnimeFTW.tv encoder',
    author = 'godofgrunts',
    author_email = 'dergottdergrunten@gmail.com',
    options = {'build_exe': {'include_files':includefiles}}, 
    executables = [Executable('hbftw-encoder.py', icon="icon.ico")]
)