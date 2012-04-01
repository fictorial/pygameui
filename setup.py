#!/usr/bin/env python

# Use 'distribute', a fork of 'setuptools'.
# This seems to be the recommended tool until 'distutils2' is completed.
# See: http://pypi.python.org/pypi/distribute

import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

# Find the version from the package metadata.

import os
import re

package_version = re.search(
    "__version__ = '([^']+)'",
    open(os.path.join('pygameui', '__init__.py')).read()).group(1)

# Resources
# - package_data is what to install. MANIFEST.in is what to bundle.
#   The distribute documentation says it can determine what data files to
#   include without the need of MANIFEST.in but I had no luck with that.
# - We find the bundled resource files at runtime using the pkg_resources
#   module from setuptools. Thus, setuptools is also a dependency.

# Dependencies
# - While Pygame is listed as a dependency, you should install it separately to
#   avoid issues with libpng and others.
#   See: http://www.pygame.org/install.html

setup(
    name='pygameui',
    version=package_version,
    author='Brian Hammond',
    author_email='brian@fictorial.com',
    install_requires=['setuptools', 'pygame>=1.9.1'],
    packages=['pygameui'],
    package_data={'pygameui': ['resources/*/*']},
    scripts=['bin/pygameui-kitchensink.py'],
    description='GUI framework for Pygame',
    keywords="UI GUI Pygame button scrollbar progress slider user interface",
    license='MIT',
    url='https://github.com/fictorial/pygameui',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Desktop Environment',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Software Development :: Widget Sets'
    ]
)
