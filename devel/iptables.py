import os
import re
import subprocess

def _get_networking_stats():

    proc = subprocess.Popen(['which','iptables'], stdout=subprocess.PIPE, close_fds=True)
    proc = proc.communicate()[0]

    if(not 'iptables' in proc):

        print 'Installing iptables..'
        installer = ""

        proc = subprocess.Popen(['which','yum'], stdout=subprocess.PIPE, close_fds=True)
        proc = proc.communicate()[0]
        if('yum' in proc): installer = proc

        if(not installer):
                        
            proc = subprocess.Popen(['which','apt-get'], stdout=subprocess.PIPE, close_fds=True)
            proc = proc.communicate()[0]
            if('apt-get' in proc): installer = proc

        installer = installer.replace('\n','')

        if(not installer):

            print 'Please install the iptables and re-run the agent.'
            sys.exit(0)

        os.system(installer+" install iptables")

    
    proc = subprocess.Popen(['iptables','-L','-vxn'], stdout=subprocess.PIPE, close_fds=True)
    data = proc.communicate()[0]
    
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

    for line in outbound_text.split('\n'):
    
        if("OUTPUT" in line):
            output_accept = line.split('policy ACCEPT ')[1]
            output_accept = output_accept.split(' ')
            output_accept_packets = output_accept[0]
            output_accept_bytes = output_accept[2]
            break

    outbound_traffic['output_accept_packets'] = output_accept_packets
    outbound_traffic['output_accept_bytes'] = output_accept_bytes

    output_accept_packets = 0
    output_accept_bytes = 0

    if(len(outbound_text.split('\n'))>3):

        c=0
        for line in outbound_text.split('\n'):
            
            if(c>3 and c<len(outbound_text.split('\n'))-1):
                output_accept_packets += int(line.split(' ')[0])
                output_accept_bytes += int(line.split(' ')[1])
                
            c+=1

    if(output_accept_packets>0): outbound_traffic['output_accept_packets'] = output_accept_packets
    if(output_accept_bytes>0): outbound_traffic['output_accept_bytes'] = output_accept_bytes

    print 'outbound_traffic', outbound_traffic


    #XXXXXX
                                                                
    forward_traffic = {}

    #for line in forward_text.split('\n'):
    #    print line

    # XXX reset iptables


    return


_get_networking_stats()
