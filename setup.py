#!/usr/bin/env python
import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='us_ignite',
      version='0.1.0',
      description='',
      long_description=README,
      author='',
      author_email='',
      license='BSD License',
      url='',
      include_package_data=True,
      package_data={
          'us_ignite': []
      },
      zip_safe=False,
      scripts=[],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      packages=find_packages(exclude=['tests']),
      install_requires=[])
