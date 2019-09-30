#!/usr/bin/python3
# -*- coding: utf-8 -*-

# usage:
# python Sender.py RECEIVER_IP RECEIVER_PORT FILE_SENT MWS MSS GAMMA P_DROP P_DELAY MAX_DELAY SEED

import sys
import time
from socket import *
from copy import copy
import threading

from header import Header
from packet import Packet
from infrastructures import *

from_port = 8848
from_ip = '127.0.0.1'
Fr_IP = '127.0.0.1'
logged = 'logged.txt'
Fr_PORT = 8888
RECEIVER_STATUS = {0: 'not_connected', 1: 'syn acked',2: 'connection established',}
class Part_2:
          def __init__(self,rc_ip = Fr_IP,rc_port = Fr_PORT):
                    #For starters,we build the srever,including the port_num nad IP address
                    self.receiver = socket(AF_INET,SOCK_DGRAM)
                    self.receiver.bind((from_ip,from_port))
                    self.rc_ip = rc_ip
                    self.rc_port = rc_port
                    #In addition to IP and numbers
                    #we need to creat seq,ack,status to me attected and so forth
                    self.seq_num = 0
                    self.ack_num = 0
                    self.memo = {}
                    self.status = 0
                    self.startt = time.time()
                    self.logger = Logger(logged)
          def info_check(self):
                    header = Header()
                    #This should be added!
                    received_header, received_data, source_ip, source_port, received_time = receive_packet(self.receiver, logger=self.logger)
                    if not received_header:
                              return True
                    
                    self.receiver.connect((source_ip, source_port))
                    if received_header.syn == 1 and received_header.ack == 0:
                              self.isn = header.isn
                              header.ack_num = received_header.seq_num+1
                              self.ack_num = received_header.seq_num+1
                              self.seq_num = header.seq_num
                              header.ack = 1
                              header.syn = 1
                              self.status = 1
                              send_packet(self.receiver, header, logger=self.logger)
                              #THis          send_packet()



                              #judge_1 = self.status
                              #judge_2 = received_header.syn
                              #judge_3 = received_header.ack
                    
                    elif self.status == 1 and received_header.syn ==2 and received_header.ack == 1:
                              
                              self.seq_num = received_header.ack_num
                              self.data_num = b''
                              self.status = 2

                    
                    elif self.status == 2 and received_header.fin == 1:
                                        
                              self.logger.data_size = len(self.data_num)
                              with open(file_name,'wb') as f:
                                        f.write(self.data_num)
                              header.ack = 1
                              header.ack_num = received_header.seq_num+1
                              self.ack_num = header.ack_num
                              header.seq_num = self.seq_num
                              send_packet(self.receiver, header, logger = self.logger)
                              header = Header()
                              header.fin = 1
                              header.seq_num = self.seq_num
                              header.ack_num = self.ack_num
                              send_packet(self.receiver, header, logger = self.logger)
                              #Function          
                              self.logger.receiver_conclude()
                              return False

                    elif self.status == 2:
                                        
                              if len(received_data) > 0:
                                        self.logger.num_segments = self.logger.num_segments+1
                              if received_header.seq_num in self.memo or received_header.seq_num < self.ack_num:
                                        self.logger.dup_count = self.logger.dup_count + 1
                                        if len(self.memo) > 0:
                                                  check_next = received_header.seq_num+len(received_data)
                                                  while check_next in self.memo:
                                                            buffer_load = self.memo[check_next]
                                                            self.data_num = self.data_num + buffer_load
                                                            check_next = check_next + len(buffer_load)
                                                            self.ack_num = self.ack_num + len(buffer_load)
                              elif received_header.seq_num > self.ack_num:
                                        print('Here is stage 3')        
                                        self.memo[received_header.seq_num] = received_data

                              print('here is the start of the header')
                              header = Header()
                              header.ack = 1
                              header.ack_num = self.ack_num
                              header.seq_num = self.seq_num
                              send_packet(self.receiver, header, logger = self.logger)







                                        

                                                  
                              











                    return True                    
                                                  
                                                            
if __name__  == '__main__':
          if len(sys.argv) != 3:
                    print('Error')
                    sys.exit()
          
          else:
                    print('THis is the console')
                    Fr_PORT,file_name = sys.argv[1:]
                    
                    receiver = Part_2()
                    keepalive = True
                    while keepalive:
                              keepalive = receiver.info_check()
