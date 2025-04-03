"""
Test the S3 connection. This takes an endpoint URL and prints all 
the objects at that endpoint.
"""

import os
import sys
import argparse

from src import S3Instance

__author__ = 'Rob Edwards'





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-e', help='endpoint', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    s3 = S3Instance(url=args.e)
    print(f"Endpoint: {s3.endpoint}")
    print(f"Bucket: {s3.get_bucket_name()}")
    print(f"Prefix: {s3.get_prefix()}")
    print()
    print("Objects:")
    print("\n".join(s3.get_all_objects()))


