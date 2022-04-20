#  """Copyright (c) 2020-2021. This file and the project containing this file is the sole property of
#                                   Tsanct Technologies Pvt Ltd (Technisanct).
#  NOTICE:  All information contained herein is, and remains the property of Technisanct.
#  The intellectual and technical concepts contained herein are proprietary to Technisanct and
#  may/may not be covered by Indian and Foreign Patents, patents in process, and are protected by trade secret
#  or copyright law. Dissemination of this information or reproduction of this material is strictly forbidden
#  unless prior written permission is obtained from Technisanct.  Access to the source code
#   contained herein is hereby forbidden to anyone except current Technisanct employees, managers
#   or contractors who have executed Confidentiality and Non-disclosure agreements explicitly covering such access.
#  The copyright notice above does not evidence any actual or intended publication or disclosure  of  this source
#  code, which includes information that is confidential and/or proprietary, and is a trade secret, of
#  Technisanct.   ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC  PERFORMANCE, OR PUBLIC
#  DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS WRITTEN CONSENT OF Technisanct IS
#  STRICTLY PROHIBITED, AND IN VIOLATION OF APPLICABLE LAWS AND INTERNATIONAL TREATIES. THE RECEIPT OR
#  POSSESSION OF THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS TO REPRODUCE,
#  DISCLOSE OR DISTRIBUTE  ITS CONTENTS, OR TO MANUFACTURE, USE, OR SELL ANYTHING THAT IT  MAY DESCRIBE, IN WHOLE
#  OR IN PART."""

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
	long_description = "\n" + fh.read()


VERSION = '0.0.4'
DESCRIPTION = 'Technisanct Integrite Packages'
LONG_DESCRIPTION = 'Technisanct Integrite Packages'

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