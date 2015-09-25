#!/usr/bin/env python

"""Extracts files from a pcap file containing a (fragmented) HTTP download
   or stream
"""

# example usage:
# justniffer -f myfile.pcap  -l "%response" -e 'extract_file.py output.file'

import argparse
import os
import re
import sys


__author__ = "Peter Mosmans"
__copyright__ = "Copyright 2015, Go Forward"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Peter Mosmans"
__contact__ = "support@go-forward.net"
__status__ = "Development"

eol_string = '\r\n'
extension = 'part'
partial = False
verbose = False


def parse_arguments():
    global verbose
    global partial
    parser = argparse.ArgumentParser()
    parser.add_argument('output', help='name of output file')
    parser.add_argument('-p', '--partial', action='store_true',
                        help='write partial files')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    args = parser.parse_args()
    partial = args.partial
    verbose = args.verbose
    if args.output:
        return args.output


def create_file(output_file):
    if os.path.exists(output_file):
        if verbose:
            print '{0} already exists - appending/overwriting...'. \
                format(output_file)
        f = file(output_file, 'r+')
    else:
        f = file(output_file, 'w')


def parse_stream(output_file):
    content = False
    offset = -1
    filename = ''
    for line in sys.stdin:
        response = re.search('^(HTTP/.\.. )(\d\d\d)(.*)', line)
        if response:
            offset = 0
            if verbose:
                print 'HTTP response {0} detected'.format(response.group(2))
        content_range = re.search('^(Content-Range: bytes )(\d*)-(\d*)', line)
        if content_range:
            filename = '{0:0>8d}-{1:0>8d}.{2}'.format(
                int(content_range.group(2)), int(content_range.group(3)),
                extension)
            offset = int(content_range.group(2))
        if (line == eol_string) and (offset >= 0):
            content = True
        if content:
            if partial and content_range:
                with open(filename, 'a') as f:
                    f.write(line)
                    if verbose:
                        print 'writing {1} bytes to {0}'.format(filename,
                                                                len(line))
            with open(output_file, 'r+') as f:
                if verbose:
                    print 'opening {0}, seeking to {1}, writing {2} bytes'. \
                        format(output_file, offset, len(line))
                    f.seek(offset, 0)
                    f.write(line)
                    offset = offset + len(line)


def main():
    output_file = parse_arguments()
    create_file(output_file)
    parse_stream(output_file)


if __name__ == "__main__":
    main()
