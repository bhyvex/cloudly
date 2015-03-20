import os
import re

data1 = """Chain INPUT (policy ACCEPT 2606360 packets, 1157611388 bytes)
pkts bytes target prot opt in out source destination
716412 215078536 all -- eth0 * 0.0.0.0/0 0.0.0.0/0

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target prot opt in out source destination

Chain OUTPUT (policy ACCEPT 2568282 packets, 1334805872 bytes)
pkts bytes target prot opt in out source destination
678334 392273020 all -- * eth0 0.0.0.0/0 0.0.0.0/0
"""

data2 = """Chain INPUT (policy ACCEPT 7176 packets, 488039 bytes)
pkts bytes target prot opt in out source destination
7194 489261 all -- eth0 * 0.0.0.0/0 0.0.0.0/0

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target prot opt in out source destination

Chain OUTPUT (policy ACCEPT 7161 packets, 5772399 bytes)
pkts bytes target prot opt in out source destination
7161 5772399 all -- * eth0 0.0.0.0/0 0.0.0.0/0
"""

data3 = """Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target prot opt in out source destination
25576 1430552 all -- eth0 * 0.0.0.0/0 0.0.0.0/0
78644 4415632 ACCEPT all -- * * 0.0.0.0/0 0.0.0.0/0 state RELATED,ESTABLISHED
499 39920 ACCEPT icmp -- * * 0.0.0.0/0 0.0.0.0/0
3 360 ACCEPT all -- lo * 0.0.0.0/0 0.0.0.0/0
3 156 ACCEPT tcp -- * * 0.0.0.0/0 0.0.0.0/0 state NEW tcp dpt:22
8938 728746 REJECT all -- * * 0.0.0.0/0 0.0.0.0/0 reject-with icmp-host-prohibited

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
pkts bytes target prot opt in out source destination
0 0 REJECT all -- * * 0.0.0.0/0 0.0.0.0/0 reject-with icmp-host-prohibited

Chain OUTPUT (policy ACCEPT 25765 packets, 44644747 bytes)
pkts bytes target prot opt in out source destination
"""

data4 = """Chain INPUT (policy ACCEPT 17 packets, 1175 bytes)
    pkts      bytes target     prot opt in     out     source               destination

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
    pkts      bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 12 packets, 9943 bytes)
    pkts      bytes target     prot opt in     out     source               destination
"""

data5 = """Chain INPUT (policy ACCEPT 3355 packets, 628519 bytes)
    pkts      bytes target     prot opt in     out     source               destination

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
    pkts      bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 2973 packets, 3130420 bytes)
    pkts      bytes target     prot opt in     out     source               destination
"""

def parse_output(data):

    inbound_text = ""
    outbound_text = ""
    forward_text = ""
    
    psc = 0
    for line in data.split('\n'):

        if(psc==0):
            if(line): inbound_text += line+"\n"
        if(psc==1):
            if(line): forward_text += line+"\n"
        if(psc==2):
            if(line): outbound_text += line+"\n"

        if(len(line)==0): psc += 1

    #print '-'*10
    #print 'inbound_text', inbound_text
    #print '-'*10
    #print 'forward_text', forward_text
    #print '-'*10
    #print 'outbound_text', outbound_text
    #print '-'*10

    inbound_traffic = {}

    for line in inbound_text.split('\n'):
        if("INPUT" in line):
            input_accept = line.split('policy ACCEPT ')[1]
            input_accept = input_accept.split(' ')
            input_accept_packets = input_accept[0]
            input_accept_bytes = input_accept[2]
            break


    inbound_traffic['input_accept_packets'] = input_accept_packets
    inbound_traffic['input_accept_bytes'] = input_accept_bytes

    input_accept_packets = 0
    input_accept_bytes = 0

    if(len(inbound_text.split('\n'))>3):

        c=0
        for line in inbound_text.split('\n'):
            if(c>3 and c<len(inbound_text.split('\n'))-1):

                input_accept_packets += int(line.split(' ')[0])
                input_accept_bytes += int(line.split(' ')[1])
                
            c+=1

    if(input_accept_packets>0): inbound_traffic['input_accept_packets'] = input_accept_packets
    if(input_accept_bytes>0): inbound_traffic['input_accept_bytes'] = input_accept_bytes

    print 'inbound_traffic', inbound_traffic

    outbound_traffic = {}
    forward_traffic = {}

    return


parse_output(data1)
print '*'*80
parse_output(data2)
print '*'*80
parse_output(data3)
print '*'*80
parse_output(data4)
print '*'*80
parse_output(data5)

