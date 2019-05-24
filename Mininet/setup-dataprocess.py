#!/usr/bin/python

import os
import sys
import time
import re
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController, OVSKernelSwitch, IVSSwitch, UserSwitch
from mininet.cli import CLI
from subprocess import Popen, PIPE
import numpy

if __name__=='__main__':
    begin1 = 'sender'
    end1 = 'receiver'
    begin2 = 'A'
    end2 = 'Bytes'
    begin3 = 'A'
    end3 = 'U'
    host_number = 10
    result_time = [0]*(int(host_number)*int(host_number))
    result_file = "./results/1/Result_NEAL_C"

    for i in range(int(host_number)):
        for j in range(int(host_number)):
            file_name = 'h' + str(j+1) + '-s' + str(i+1) + '.txt'
            with open(file_name, 'r') as file:
                result = file.read().replace('\n', ' ').replace(' ', 'U').replace('-', 'A')

            timeEntry = re.search(begin1+'(.*)'+end1, result)
            if timeEntry != None:
                timeValue = re.search(begin2+'(.*)'+end2, timeEntry.group(0))
                timeValueAgain = re.search(begin3+'(.*)'+end3, timeValue.group(0))
                st = timeValueAgain.group(0)
                while timeValueAgain != None:
                    st = timeValueAgain.group(0)[:-1]
                    timeValueAgain = re.search(begin3+'(.*)'+end3, st)
                result_time[i*int(host_number)+j] = float(st[1:])

    print('All time: ')
    print(result_time)
    print('Max time: ')
    print(max(result_time))
    print('Mean time: ')
    print(sum(result_time)/len(result_time))
    print('Zero counter: ')
    print(result_time.count(0))
    
    Outfile=open(result_file, "w")
    for i in range(int(host_number)*int(host_number)):
        Outfile.write(str(result_time[i])+', ')
        if (i+1) % int(host_number) == 0:
            Outfile.write(' \n')

    Outfile.write('Max time = ' + str(max(result_time)) + '\n')
    Outfile.write('Zero counter = ' + str(result_time.count(0)) + '\n')
    Outfile.close()





