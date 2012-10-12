#!/usr/bin/python

import os, shutil, commands, getpass, sys

if os.getuid() != 0:
    exit('Try sudo ./setup.py')

spath = os.path.dirname(os.path.abspath(sys.argv[0]))
print 'Copying binary files to /usr/bin/...',
shutil.copyfile(os.path.join(spath, 'load-balancer.py'), '/usr/bin/load-balancer.py')
shutil.copyfile(os.path.join(spath, 'daemon.py'), '/usr/bin/daemon.py')
os.chmod('/usr/bin/load-balancer.py', 0775)
os.chmod('/usr/bin/daemon.py', 0775)
print 'OK!'
print 'Updating rc.d...',
shutil.copyfile(os.path.join(spath, 'load-balancer'), '/etc/init.d/load-balancer')
os.chmod('/etc/init.d/load-balancer', 0775)
commands.getoutput('update-rc.d load-balancer defaults')
print 'OK!'
print 'Configuring /usr/local/etc/cloud.cfg:'
nodes = raw_input(u'Number of hosts [5]: ')
if nodes == '':
    nodes = '5'
while True:
    host = raw_input(u'Host IP address: ')
    if host != '':
	break
    print 'Please enter host IP address!'
user = raw_input(u'Username [root]: ')
if user == '':
    user = 'root'
while True:
    pasw = getpass.getpass(u'Password: ')
    pasw1 = getpass.getpass(u'Re-enter your password: ')
    if pasw == pasw1 and pasw != '':
	break
    elif pasw == pasw1 and pasw == '':
	print 'Password is empty!'
    elif pasw != pasw1:
	print 'Passwords are different!'
log_balancer = raw_input(u'Enable logging [yes]/no: ')
if log_balancer == '' or log_balancer == 'yes':
    log_balancer = 'yes'
    log_path = raw_input(u'Path to logfile [/var/log/]: ')
    if log_path == '':
	log_path = '/var/log/'
else:
    log_path = '/var/log/'
print 'Creating /usr/local/etc/cloud.cfg...',
if os.path.exists('/usr/local/etc/cloud.cfg'):
    print 'alredy exist!'
else:
    cloud = open('/usr/local/etc/cloud.cfg', 'w')
    cloud.write('NODES %s\nHOST %s\nUSER %s\nPASS %s\nLOG_BALANCER %s\nLOG_PATH %s' % (nodes, host, user, pasw, log_balancer, log_path))
    cloud.close()
    print 'OK!'
print 'Creating /usr/local/etc/dependencies.cfg...',
if os.path.exists('/usr/local/etc/dependencies.cfg'):
    print 'already exist!'
else:
    dep = open('/usr/local/etc/dependencies.cfg', 'w')
    dep.close()
    print 'OK!'
deltmp = raw_input(u'Delete all temporary files? [yes]/no: ')
if deltmp == '' or deltmp == 'yes':
    shutil.rmtree(spath)