import sys
import memo

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

def requirements():
    install_requires = []
    with open('requirements.txt') as f:
        for line in f:
            install_requires.append(line.strip())

    return install_requires


setup(
    name='memo',
    version=memo.__version__,
    description=memo.__doc__.strip(),
    long_description=readme(),
    url='https://github.com/mackong/memo',
    author=memo.__author__,
    author_email='mackonghp@gmail.com',
    license=memo.__license__,
    packages=['memo'],
    entry_points={'console_scripts': ['memo=memo.memo:main']},
    install_requires=requirements(),
    keywords=['memo', 'note taking'],
)
