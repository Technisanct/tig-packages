from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
	long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Technisanct integrated packages'
LONG_DESCRIPTION = 'Technisanct integrated packages'

# Setting up
setup(
	name="tig-packages",
	version=VERSION,
	author="Technisanct",
	author_email="<shibi@technisanct.com>",
	description=DESCRIPTION,
	long_description_content_type="text/markdown",
	long_description=long_description,
	packages=find_packages(),
	install_requires=['boto3'],
	keywords=['python', 'package', 's3'],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent"
	]
)