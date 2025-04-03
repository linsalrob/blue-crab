"""
Read a pod5 file from the  S3 endpoint and list some information in it.
"""

import os
import sys
import argparse
import pod5 as p5
from src import S3Instance

__author__ = 'Rob Edwards'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-e', help='S3 endpoint', required=True)
    parser.add_argument('-o', help='S3 object name', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    s3 = S3Instance(url=args.e)
    pfile = s3.get_s3_file(args.o)

    with p5.Reader(pfile) as reader:
        for read in reader.reads():
            print(f"read_id {read.read_id}")
            print(f"channel {read.pore.channel}")
            print(f"well {read.pore.well}")
            print(f"pore_type {read.pore.pore_type}")
            print(f"read_number {read.read_number}")
