#!/usr/bin/python

import os
import sys
import time
import re
import numpy as np
import datetime
import random
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController, OVSKernelSwitch, IVSSwitch, UserSwitch, OVSController
from subprocess import Popen, PIPE
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

def setCommand(hnum, hid, sid, wl, bw):
    para_file = "host-parameters.txt"
    host_number = hnum
    host_id = hid
    server_id = sid
    communication_loadsize = 0
    communication_bandwidth = 0
    Outfile=open(para_file, "a+")
    Outfile.write(str(hnum) + ' | ' + str(hid) + ' | ' + str(sid) + ' | ' + str(wl) + ' | ' + str(bw) + "\n")
    
    para_number = int(host_number)*int(host_number)
    loadsize_array = []
    bandwidth_array = []
    for i in range(host_number):
        loadsize_array = loadsize_array +wl[i]
    for i in range(host_number):
        bandwidth_array = bandwidth_array + bw[i]
    Outfile.write(str(loadsize_array) + '\n')
    Outfile.write(str(bandwidth_array) + '\n')

    sync_time = int(host_number)
    port_head = 500
    address_head = '10.0.0.'
    cmdHead_s = 'sudo stdbuf -i0 -o0 -e0 iperf3 -s -i 0 -p '
    cmdTail_s = '.txt & '
    cmdFull_s = ''
    cmdHead_c = 'sudo stdbuf -i0 -o0 -e0 iperf3 -c '
    cmdTail_c1 = ' -l 8192 -i 0 & '
    cmdTail_c2 = ' -l 2 -i 0 & '
    cmdFull_c = ''
    
    host = 'h' + str(host_id)
    server = 's' + str(sid)
    outputFile_s = ' --logfile ' + host + '-' + server + cmdTail_s
    port = str(port_head + int(sid))
    cmd_s = cmdHead_s + port + outputFile_s
    cmdFull_s = cmdFull_s + cmd_s
    Outfile.write(cmdFull_s + '\n')
    
    host = 'h' + str(host_id)
    server = 's' + str(sid)
    port = str(port_head + int(sid))
    address_target = address_head + str(sid)
    if int(host_id) != hnum:
        outputFile_c = cmdTail_c1
        communication_loadsize = (float(loadsize_array[(int(host_id)-1)*int(host_number)+sid-1]))/1024
        communication_bandwidth = float(bandwidth_array[(int(host_id)-1)*int(host_number)+sid-1])*8.0/1024
        cmd_c = cmdHead_c + address_target + ' -p ' + str(port_head+int(host_id)) + ' -n ' + str(communication_loadsize) + 'k' + outputFile_c
    else:
        outputFile_c = cmdTail_c2
        communication_loadsize = (float(loadsize_array[(int(host_id)-1)*int(host_number)+sid-1]))
        communication_bandwidth = float(bandwidth_array[(int(host_id)-1)*int(host_number)+sid-1])*8.0
        cmd_c = cmdHead_c + address_target + ' -p ' + str(port_head+int(host_id)) + ' -n ' + str(communication_loadsize) + '' + outputFile_c        
    if float(communication_loadsize) > 0.0 and float(communication_bandwidth) > 0.0:
        cmdFull_c = cmdFull_c + cmd_c

    Outfile.write(cmdFull_c + '\n')
    
    Outfile.close()
    return cmdFull_s, cmdFull_c

def setupNetwork(totalHost):
    net = Mininet( topo=None, link=TCLink, build=False, ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=Controller, protocol='tcp', port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)

    bw_value = []
    bw_setting = [0]*totalHost
    bw_file = './settings/bw/bw_1_1_1'
    f = open(bw_file, 'r')
    host_bw_lines = f.readlines()
    f.close()
    bw_value = map(float, host_bw_lines[0].split(','))
    for i in range(totalHost):
        bw_setting[i] = (bw_value[i]*8)/1024/1024

    info( '*** Add links\n')
    net.addLink(h1, s1, bw=bw_setting[0])
    net.addLink(h2, s1, bw=bw_setting[1])
    net.addLink(h3, s1, bw=bw_setting[2])
    net.addLink(h4, s1, bw=bw_setting[3])
    net.addLink(h5, s1, bw=bw_setting[4])
    net.addLink(h6, s1, bw=bw_setting[5])
    net.addLink(h7, s1, bw=bw_setting[6])
    net.addLink(h8, s1, bw=bw_setting[7])
    net.addLink(h9, s1, bw=bw_setting[8])
    net.addLink(h10, s1, bw=bw_setting[9])

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    
    net.pingAll()
    
    print "Read server setup for communication workload and bandwidth."
    workload = []
    bandwidth = []
    workload_file = './settings/1/NEAL_V'
    bandwidth_file = './settings/1/NEAL_B'
    f = open(workload_file, 'r')
    host_workload_lines = f.readlines()
    f.close()
    f = open(bandwidth_file, 'r')
    host_bandwidth_lines = f.readlines()
    f.close()
    for i in range(totalHost):
        workload.append(map(float, host_workload_lines[i].split(',')))
        bandwidth.append(map(float, host_bandwidth_lines[i].split(',')))

    print "Run scripts in the background on hosts."
    for h in range(1, totalHost+1):
        for s in range(1, totalHost+1):
            hostID = h
            serverID = s
            server_cmd, client_cmd = setCommand(totalHost, hostID, serverID, workload, bandwidth)
            hx = net.get('h' + str(hostID))
            hx.cmd(server_cmd)
            sys.stdout.flush()
            print 'Setup server: h' + str(h) + '-s' + str(s) + '...'

    for h in range(1, totalHost+1):
        for s in range(1, totalHost+1):
            hostID = h
            serverID = s
            server_cmd, client_cmd = setCommand(totalHost, hostID, serverID, workload, bandwidth)
            hx = net.get('h' + str(hostID))
            hx.cmd(client_cmd)
            sys.stdout.flush()
            print 'Setup client: h' + str(h) + '-c' + str(s) + '...'

    print('======>>>>>>' + str(datetime.datetime.now()) + '<<<<<<======')
    b = np.array(bandwidth)
    w = np.array(workload)
    b[b == 0] = 1
    r = w / b
    print("Theory Result = " + str(np.amax(r)))
    raw_input('Press enter to exit...(eql)')

if __name__=='__main__':
    host_total_number = 10
    para_file = "host-parameters.txt"
    print "==============================================================="
    os.system("sudo mn -c")
    print "==============================================================="
    setLogLevel('info')
    open(para_file, "w").close()
    for i in range(host_total_number):
        for j in range(host_total_number):
            file_name = 'h' + str(j+1) + '-s' + str(i+1) + '.txt'
            open(file_name, 'w').close()

    setupNetwork(host_total_number)


