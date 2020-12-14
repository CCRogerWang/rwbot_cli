# source venv/bin/activate
# pip install --editable . #install command

from setuptools import setup

setup(
    name = 'iosbot',
    version='0.0.1',
    py_modules = ['iosbot'],
    install_requires = [
        'Click'
    ],
    entry_points = '''
        [console_scripts]
        iosbot = iosbot_main:iosbot
    '''
)