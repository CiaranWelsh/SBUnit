
from setuptools import setup

MAJOR = 0
MINOR = 0
MICRO = 1

VERSION = F"{MAJOR}.{MINOR}.{MICRO}"

setup(
    name='sbunit',
    version=VERSION,
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Ciaran Welsh',
    author_email='cwelsh2@uw.edu',
    url='https://github.com/CiaranWelsh/SBUnit',
    keywords=['unittest', "systems biology", "SBML", "SEDML"],
    install_requires=open('requirements.txt').read().split('\n'),
    packages=['sbunit'],
    package_dir={'sbunit': 'sbunit'},
)
