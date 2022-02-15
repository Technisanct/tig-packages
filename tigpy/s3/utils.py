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

import boto3


class Utils():
	"""
	s3 utils class
	"""

	def __init__(self, access_key, secret_key):
		"""

		:param access_key: s3 access key
		:type access_key: str
		:param secret_key: s3 secret key
		:type secret_key: str
		"""
		self.access_key = access_key
		self.secret_key = secret_key

	@staticmethod
	def _get_bucket_and_prefix(path):
		"""
		split the s3 path to bucket and key
		@param path: s3 path
		@type path: string
		@return: s3 bucket and key
		@rtype: tuple
		"""
		_path = path.split('/')
		bucket, prefix = _path[2], '/'.join(_path[3:])
		return bucket, prefix

	def get_client(self):
		"""
		to get s3 client object
		@return: s3 resource object
		@rtype: botocore.client.S3 object
		"""
		client = boto3.client(
			's3',
			aws_access_key_id=self.access_key,
			aws_secret_access_key=self.secret_key,
		)
		return client

	def get_resource(self):
		"""
		to get s3 resource
		@return: s3 resource object
		@rtype: boto3.resources.factory.s3.ServiceResource object
		"""
		session = boto3.Session(
			aws_access_key_id=self.access_key,
			aws_secret_access_key=self.secret_key,
		)
		s3 = session.resource('s3')
		return s3

	def get_data(self, path):
		"""
		to get s3 data in string format
		@param path: s3 path
		@type path: string
		@return: file content in s3
		@rtype: string
		"""
		resource = self.get_resource()
		bucket_name, key = self._get_bucket_and_prefix(path)
		content_object = resource.Object(bucket_name, key)
		file_content = content_object.get()['Body'].read().decode('utf-8')
		return file_content

	def store_data(self, path, content):
		"""
		@param path: s3 path
		@type path: string
		@param content: content to store
		@type content: bytes
		@return: is success bool value and error message
		@rtype: tuple
		"""

		is_success, error = (True, None)
		resource = self.get_resource()
		bucket_name, key = self._get_bucket_and_prefix(path)
		try:
			s3object = resource.Object(bucket_name, key)
			s3object.put(
				Body=content,
				ServerSideEncryption='AES256',
			)
		except Exception as e:
			is_success, error = False, str(e)
		finally:
			return is_success, error

	def move_data(self, source_path, destination_path):
		"""
		move data from one location to other
		@param source_path: source s3 path
		@type source_path: string
		@param destination_path: destination s3 path
		@type destination_path: string
		@return: is success bool value and error message
		@rtype: tuple
		"""

		is_success, error = (True, None)
		try:
			resource = self.get_resource()
			source_bucket, source_key = self._get_bucket_and_prefix(source_path)
			destination_bucket, destination_key = self._get_bucket_and_prefix(destination_path)
			copy_source = {
				'Bucket': source_bucket,
				'Key': source_key
			}
			resource.meta.client.copy(copy_source, destination_bucket, destination_key)
			self.delete_file(source_path)
		except Exception as e:
			is_success, error = False, str(e)
		finally:
			return is_success, error

	def delete_file(self, path):
		"""
		to delete a file from s3
		@param path: s3 path
		@type path: string
		@return: is success bool value and error message
		@rtype: tuple
		"""
		is_success, error = (True, None)
		try:
			resource = self.get_resource()
			bucket_name, key = self._get_bucket_and_prefix(path)
			resource.Object(bucket_name, key).delete()
		except Exception as e:
			is_success, error = False, str(e)
		finally:
			return is_success, error

	def get_files_in_directory(self, path, file_filter=None):
		"""
		return files in an s3 directory
		@param path: s3 path
		@type path: string
		@param file_filter: filter text
		@type file_filter: string
		@return: list of file path
		@rtype: list
		"""
		resource = self.get_resource()
		bucket_name, prefix = self._get_bucket_and_prefix(path)
		bucket = resource.Bucket(bucket_name)
		for object_summary in bucket.objects.filter(Prefix=prefix):
			if file_filter:
				if object_summary.key.endswith(file_filter):
					yield object_summary.key
			else:
				yield object_summary.key

