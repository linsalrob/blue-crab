"""
Read the buckets on an S3 instance and return a list of buckets/objects
"""

import os
import sys
sys.path = [p for p in sys.path if "py-botocore" not in p]
import boto3
from botocore.exceptions import ClientError
from io import BytesIO
from urllib.parse import urlparse

__author__ = 'Rob Edwards'


class S3Exception(Exception):
    """
    An error accessing something via S3

    :param message: explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class S3Instance:
    def __init__(self, url=None, endpoint=None, bucket_name=None, prefix=None, verbose=False):
        """
        Instantiate the class
        """

        if url:
            parsed = urlparse(url)
            self.endpoint = f"{parsed.scheme}://{parsed.netloc}/"
            sp = parsed.path.strip('/').split('/')
            bucket_name = sp[0]
            prefix = '/'.join(sp[1:]+['']) # this appends a trailing '/' which is needed for directories
        elif endpoint:
            self.endpoint = endpoint
        else:
            raise S3Exception("FATAL: Please provide an endpoint")
    
        self.session = boto3.session.Session()
        self.s3 = self.session.client(
            service_name='s3',
            endpoint_url=self.endpoint,
        )
        
        if bucket_name:
            self.set_bucket_name(bucket_name)
        if prefix:
            self.set_prefix(prefix)
        
        self.all_objects = set()
        if self.bucket_name and self.prefix:
            self.get_all_objects()

    def bucket_exists(self, bucket_name):
        """
        Check whether the bucket exists in our endpoint. Returns True if it does
        """
        try:
            self.s3.head_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            return False


    def set_bucket_name(self, bucket_name):
        """
        Set the bucket name. 
        If that is a valid bucket we save that name, otherwise we raise an
        error.
        
        :param: bucket_name the name to set
        :return: the current bucket name
        """

        if self.bucket_exists(bucket_name):
            self.bucket_name = bucket_name
        else:
            raise S3Exception(f"FATAL: The bucket {bucket_name} does not exist at the endpoint {self.endpoint}")

    def get_bucket_name(self):
        """
        Return the bucket name
        """
        return self.bucket_name

    def prefix_exists(self, prefix):
        """
        Test whether the prefix exists in the bucket
        """
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, MaxKeys=1)
        return 'Contents' in response

    def set_prefix(self, prefix):
        """
        Set the prefix
        If that is a valid bucket we save that name, otherwise we raise an
        error.
        
        :param: prefix the name to set
        :return: the current bucket name
        """

        if self.prefix_exists(prefix):
            self.prefix = prefix
        else:
            raise S3Exception(f"FATAL: The prefix {prefix} does not exist in the bucket {self.bucket_name}")

    def get_prefix(self):
        """
        Return the prefix name
        """
        return self.prefix

    def get_all_objects(self):
        """
        Get the objects in the bucket and and at prefix
        """

        if self.all_objects:
            return self.all_objects
        if not self.endpoint:
            raise S3Exception(f"Please define an endpoint before you start")
        
        if not self.bucket_name:
            raise S3Exception(f"Please define a bucket before you get all objects")

        for obj in self.s3.list_objects(Bucket=self.bucket_name, Prefix=self.prefix)['Contents']:
            self.all_objects.add(obj['Key'])
        return self.all_objects


    def get_s3_file(self, filename):
        """
        This returns a file-like object that you can read with "with open"
        """
        response = self.s3.get_object(Bucket=self.bucket_name, Key=filename)
        return BytesIO(response["Body"].read())

