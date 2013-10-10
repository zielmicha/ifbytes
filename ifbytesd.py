import os
import subprocess
import signal
import sys
import time

TIMEOUT = 5

children = []

def deamonize():
    os.chdir('/')
    os.umask(0o700)
    null = open('/dev/null', 'r+')
    os.dup2(null.fileno(), 0)
    os.dup2(null.fileno(), 1)
    os.dup2(null.fileno(), 2)
    if os.fork() == 0:
        os.setsid()
        if os.fork() != 0:
            os._exit(0)
    else:
        os._exit(0)

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

def keep_process(args, output):
    signal.signal(signal.SIGALRM, alarm_handler)

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=open('/dev/null', 'w'))

    while True:
        try:
            signal.alarm(TIMEOUT)
            line = proc.stdout.readline()
            signal.alarm(0)
        except Alarm:
            print 'Timed out.'
            break

        if not line:
            break

        output.write(line)

    proc.terminate()
    proc.wait()

def main():
    output = sys.argv[1]
    file = open(output, 'a', 1)
    deamonize()
    while True:
        keep_process(sys.argv[2:], file)
        time.sleep(3)

if __name__ == '__main__':
    main()
