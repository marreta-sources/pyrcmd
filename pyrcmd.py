#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import content

import paramiko
import time

class SSH(object):
    """ Connect and execute command to a client server

        Attributes:
        IP          IP or Hostname to client server
        User        User used to connect using ssh
        passwd      Password used to connect to ssh

        Return: Disctionary (Array) with Return Code, Std output and Std Error
    """
    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.user = user
        self.passwd = passwd

    def execute(self, command):
        seconds_to_timeout = 1
        while True:
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(
                        paramiko.AutoAddPolicy())
                client.connect(self.ip, username=self.user, password=self.passwd)
                break
            except paramiko.AuthenticationException:
                raise ValueError("TESTE")
            except paramiko.NoValidConnectionsError:
                raise ValueError("TESTE2")
            except:
                seconds_to_timeout += 1
                time.sleep(2)
            if seconds_to_timeout == 30:
                raise ValueError('TESTE4')
        command_response = { 'return_code' :'', 'stdout' : '', 'stderr' : '' }
        chan = client.get_transport().open_session()
        chan.exec_command(command=command)
        command_response['return_code'] = chan.recv_exit_status()
        while chan.recv_ready():
            command_response['stdout'] += chan.recv(1024)

        while chan.recv_stderr_ready():
            command_response['stderr'] += chan.recv(1024)

        print ("output")
        print (command_response['stdout'])
        print ("error")
        print (command_response['stderr'])
        print ("Exit Code")
        print (command_response['return_code'])
        print ("fim")
        client.close()
        return command_response
