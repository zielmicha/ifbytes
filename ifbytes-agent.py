#!/usr/bin/env python
import time
import sys

WAIT_TIME = 3

def get_bytes():
    lines = open('/proc/net/dev').readlines()
    for line in lines[2:]:
        fields = line.split()
        yield (fields[0].rstrip(':'), int(fields[1]), int(fields[9]))

def main():
    while True:
        print(str(time.time()) + ' ' + ' '.join(
            ','.join(map(str, dev)) for dev in get_bytes() ))
        sys.stdout.flush()
        time.sleep(WAIT_TIME)

if __name__ == '__main__':
    main()
