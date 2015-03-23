import os, sys
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
        # XXX make iptables init here
    
    # XXX pull iptables data
    # XXX reset iptables counters
  
    return "XXX"

network_stats = _get_networking_stats()
  
