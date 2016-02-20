from setuptools import setup

setup(
    name='oscm',
    version='0.1',
    py_modules=['oscm','initialize','generate','utils','pull_repo'],
    install_requires=[
        'Click',
        'gitpython'
    ],
    entry_points='''
        [console_scripts]
        oscm=oscm:cli
    ''',
)
