from setuptools import setup, find_packages

setup(
    name='pokerGame',
    version='0.0.1',
    author='David Girsvaldas',
    author_email='david.girsvaldas@gmail.com',
    description='Poker game engine',
    license='MIT',
    keywords='python poker engine',
    url='https://github.com/DavidGirsvaldas/pokerGame',
    packages=[pkg for pkg in find_packages() if pkg != "tests"]
)
