import os
import sys

SUDO_PWD = 'Your Password'


def cpu(pod_id, value, period=100000):
    if int(value) <= 0:
        raise ValueError('Invalid Value!')
    value = int((value / 64) * period)
    # print('cpu - id: ' + pod_id + ' - delta: ' + str(value))
    path = '/sys/fs/cgroup' + pod_id + '/cpu.max'
    # print(path)
    with open(path, 'r+') as f:
        data = f.read()
        print("Old Data: %s, New Data: %s" % (data, value))
        f.seek(0)
        f.write(str(value))
        f.truncate()


pod_id = sys.argv[1]
value = sys.argv[2]
cpu(pod_id, value)
