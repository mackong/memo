from setuptools import setup

setup(
    name='Memo',
    version='1.0',
    py_modules=['memo'],
    install_requires=[
        'click',
        'termcolor',
    ],
    entry_points='''
    [console_scripts]
    memo=memo:main
    '''
)
