import boto3


class Utils():
	"""
	s3 utils class
	"""

	def __init__(self, **kwargs):
		self.resource = self._get_resource(kwargs)
		self.client = self._get_client(kwargs)

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

	def _get_client(self, kwargs):
		"""
		to get s3 client object
		@param kwargs: list of arguments
		@type kwargs: list of dict
		@return: s3 resource object
		@rtype: botocore.client.S3 object
		"""
		client = boto3.client(
			's3',
			aws_access_key_id=kwargs['aws_access_key_id'],
			aws_secret_access_key=kwargs['aws_secret_access_key'],
		)
		return client

	def _get_resource(self, kwargs):
		"""
		to get s3 resource
		@param kwargs: list of arguments
		@type kwargs: list of dict
		@return: s3 resource object
		@rtype: boto3.resources.factory.s3.ServiceResource object
		"""
		session = boto3.Session(
			aws_access_key_id=kwargs['aws_access_key_id'],
			aws_secret_access_key=kwargs['aws_secret_access_key'],
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
		bucket_name, key = self._get_bucket_and_prefix(path)
		content_object = self.resource.Object(bucket_name, key)
		file_content = content_object.get()['Body'].read().decode('utf-8')
		return file_content

	def store_data(self, path, content):
		"""
		@param path: s3 path
		@type path: string
		@param content: content to store
		@type content: bytes
		@return: None
		@rtype: None
		"""

		bucket_name, key = self._get_bucket_and_prefix(path)
		s3object = self.resource.Object(bucket_name, key)
		s3object.put(
			Body=content,
			ServerSideEncryption='AES256',
		)

	def move_data(self, source_path, destination_path):
		"""
		move data from one location to other
		@param source_path: source s3 path
		@type source_path: string
		@param destination_path: destination s3 path
		@type destination_path: string
		@return: None
		@rtype: None
		"""

		source_bucket, source_key = self._get_bucket_and_prefix(source_path)
		destination_bucket, destination_key = self._get_bucket_and_prefix(destination_path)
		copy_source = {
			'Bucket': source_bucket,
			'Key': source_key
		}
		self.resource.meta.client.copy(copy_source, destination_bucket, destination_key)
		self.delete_file(source_path)

	def delete_file(self, path):
		"""
		to delete a file from s3
		@param path: s3 path
		@type path: string
		@return: None
		@rtype: None
		"""
		bucket_name, key = self._get_bucket_and_prefix(path)
		self.resource.Object(bucket_name, key).delete()

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
		bucket_name, key = self._get_bucket_and_prefix(path)

		# get all the files using list_objects_v2, pagination limit of 1000 is handled
		response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=key)
		files = [i['Key'] for i in response['Contents']]
		while 'NextContinuationToken' in response:
			response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=key,
			                                          ContinuationToken=response['NextContinuationToken'])
		files.extend([i['Key'] for i in response['Contents']])
		if file_filter:
			files = [_file for _file in files if file_filter in _file]
		return files