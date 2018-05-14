#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import os
import argparse

hosts = {
    'mjz': {'user':'mjz', 'host': '101.200.42.130', 'port': 22, 'desc': ''},
}

def login(name):
    host = hosts[name]
    cmd = 'ssh'
    if 'port' in host:
        cmd += ' -p ' + str(host['port'])
    if 'rsa' in host:
        cmd += ' -i ' + host['rsa']
    cmd += ' {user}@{host}'.format(user=host['user'], host=host['host'])

    print(cmd)  
    os.system(cmd)


def scp(file1, file2):
    cmd = 'scp '
    if ':' in file1:
        host = hosts[file1.split(':')[0]]
    else:
        host = hosts[file2.split(':')[0]]

    if 'port' in host:
        cmd += ' -P ' + str(host['port'])
    if 'rsa' in host:
        cmd += ' -i ' + host['rsa']

    if ':' in file1:
        cmd += ' {user}@{host}'.format(user=host['user'], host=host['host']) + ':' + file1.split(':')[1]
        cmd += ' ' + file2
    else:
        cmd += ' ' + file1
        cmd += ' {user}@{host}'.format(user=host['user'], host=host['host']) + ':' + file2.split(':')[1]

    print(cmd)
    os.system(cmd)

def listHost(name):
    if name == 'all' or not name:
        for host in hosts.items():
            print(host)
    elif name in hosts:
        print(hosts[name])
    else:
        'does not exist'

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='remote server host helper')
    ap.add_argument('-a', '--action', type=str,
                    help='remote action, ssh, scp, list host',
                    )
    ap.add_argument('-o', '--host', type=str,
                    help='host name',
                    )

    ap.add_argument('-f1', '--file1', type=str,
                    help='remote action, ssh, scp, list host',
                    )
    ap.add_argument('-f2', '--file2', type=str,
                    help='remote action, ssh, scp, list host',
                    )

    args = ap.parse_args()
    if args.action == 'ssh':
        login(args.host)
    elif args.action == 'scp':
        scp(args.file1, args.file2)
    elif args.action == 'list':
        listHost(args.host)
    
