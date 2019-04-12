from setuptools import setup

setup(
    name='lm_soundboard',
    version='0.1',
    description='A soundboard controller for NOVATION Launchpads.',
    author='Thibaud Kehler',
    license="GPLv3",
    author_email='mail@tkehler.de',
    packages=['lm_soundboard'],
    install_requires=['launchpad_py']
)
