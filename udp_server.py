import socket
import threading
import time
import os
import udp_server
from datetime import datetime

class UDPServer:

    ''' A simple UDP Server '''
    def __init__(self, host, port):

        self.host = host    # Host address
        self.port = port    # Host port
        self.sock = None    # Socket
        self.TOKEN = False  # Sending Token

    def printwt(self, msg):

        ''' Print message with current date and time '''
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[%s] %s"%(current_date_time, msg))

    def configure_server(self):

        ''' Configure the server '''
        # create UDP socket with IPv4 addressing
        self.printwt('Creating socket...')

        # bind server to the address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.printwt('Socket created:')
        self.printwt(self.sock.getsockname())
        self.printwt("Binding server to %s:%s..."%(self.host, self.port))
        self.sock.bind((self.host, self.port))
        self.printwt("Server binded to %s:%s"%(self.host, self.port))


    def handle_request(self, data, client_address):

        ''' Handle the client '''
        # handle request
        name = data.decode('utf-8')
        self.printwt("[ REQUEST from %s ]"%client_address)
        print('\n', name, '\n')

        # send response to the client
        resp = self.get_phone_no(name)
        time.sleep(3)
        self.printwt("[ RESPONSE to %s ]"%client_address)
        self.sock.sendto(resp.encode('utf-8'), client_address)
        print('\n', resp, '\n')

    def wait_for_client(self):

        ''' Wait for a client '''
        try:

            # receive message from a client
            data, client_address = self.sock.recvfrom(2048)

            # handle client's request
            self.handle_request(data, client_address)
            print(client_address)


        except OSError as err:
            self.printwt(err)

    def shutdown_server(self):

        ''' Shutdown the UDP server '''
        self.printwt('Shutting down server...')
        self.sock.close()
