from pathlib import Path

from setuptools import setup, find_packages


packagename = 'bibcode'
description = "Work with NASA/SAO ADS bibcodes on the command line."
author = 'Jonathan Sick'
author_email = 'jsick@lsst.org'
license = 'MIT'
url = 'https://github.com/jonathansick/bibcode'
classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
]
keywords = 'latex bibtex astronomy'

readme_path = Path(__file__).parent / 'README.rst'
long_description = readme_path.read_text()

# Core dependencies
install_requires = [
    'click>=6.7,<7.0',
    'uritemplate',
    'aiohttp>=3.0.0',
    'cchardet',  # recommended speed-up for aiohttp
    'aiodns',  # recommended speed-up for aiohttp
]

# Setup dependencies
setup_requires = [
    'pytest-runner>=2.11.1,<3',
    'setuptools_scm'
]

# Test dependencies
tests_require = None

# Optional/development dependencies
docs_require = None
extras_require = None

entry_points = {
    'console_scripts': [
        'bibcode = bibcode.cli.main:main',
    ]
}


setup(
    name=packagename,
    description=description,
    long_description=long_description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=classifiers,
    keywords=keywords,
    packages=find_packages(exclude=['docs', 'tests*', 'data']),
    install_requires=install_requires,
    extras_require=extras_require,
    setup_requires=setup_requires,
    tests_require=tests_require,
    use_scm_version=True,
    # package_data={},
    entry_points=entry_points,
)
