"""
Setup script for pyquanta

"""

from setuptools import setup
from setuptools import find_packages


def readme():
    """
    Extracts contents from README.md

    """
    with open('README.md') as r:
        return r.read()


def requirements():
    """
    Fetch requirements from requirements.txt

    """
    with open('requirements.txt') as req:
        return req.read().splitlines()


setup(name='pyquanta',
      version='0.2.1',
      description='Pyquanta is a python module to interact with Quanta API',
      long_description=readme(),
      license='MIT',
      url='https://github.com/quanta-computing/pyquanta',
      author="Matthieu 'Korrigan' Rosinski",
      author_email='mro@quanta-computing.com',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Utilities',

      ],
      packages=find_packages(),
      install_requires=requirements(),
  )
