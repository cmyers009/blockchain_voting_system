import socket
import threading
import time
import os
import udp_server
from mysig import message
from datetime import datetime
import pickle
from queue import Queue
import queue2
from block import Block
from blockchain import Blockchain

NUM_NODES = int(input("How many nodes are running on this network? "))

    

hostname = socket.gethostname()
host_split = hostname.split('.')
host = host_split[0]
host_split.pop(0)
nameEnd = ".".join(host_split)
MY_ID = int(host.split("-")[1])


# Static Values
MAX_VAL = 2048
#NUM_NODES = 3
#MY_ID = 0
nodes = ["node-{}".format(i) for i in range(NUM_NODES)]
#nodes = ['node-0', 'node-1', 'node-2']
#nameEnd = '.matt-test.ch-geni-net.instageni.rutgers.edu'
node_names = ['' for _ in range(NUM_NODES)]
for i in range(NUM_NODES):
    node_names[i] = nodes[i]+'.'+nameEnd

MY_NAME = node_names[MY_ID]

q = Queue()
local_blockchain = None

# Variables
current_state = -1
vote_count = 0
num_connections = 0
current_block = None
PRIORITY_ID = 0
node_ports = [0 for _ in range(NUM_NODES)]
print("# Network Node Addresses:")
for i in range(NUM_NODES):
    node_ports[i] = 64000+i
    print("\t%s: %s:%s"%(i, node_names[i], node_ports[i]))

MY_PORT = node_ports[MY_ID]
print("\n# My Address: %s:%s\n"%(MY_NAME, MY_PORT))


class UDPServerMultiClient(udp_server.UDPServer, object):
    ''' A simple UDP Server for handling multiple clients '''
    

    def __init__(self, host, port):
        super(UDPServerMultiClient, self).__init__(host, port)
        self.socket_lock = threading.Lock()
        if (MY_ID == 0):
            self.TOKEN = True

    
    def handle_request(self, data, client_address):
        def thread_find_proof():
                global local_blockchain
                block = pickle.loads(msgPayload)
                block.previous_hash = local_blockchain.chain[-1].hash
                proof = local_blockchain.proof_of_work(block)
                #print(f"Proof: {str(proof)}")
                #print(f"local_blockchain done signal {str(local_blockchain.done_signal)}")
                if proof:
                #send message to main
                    print("Found proof: ",proof)
                    payload = pickle.dumps(block)
                    self.send_request("NONCE FOUND",payload,(node_names[msgSenderID],node_ports[msgSenderID]))
                
                return
        global current_state
        global local_blockchain
        global vote_count
        global current_block
        ''' Handle the client '''

        # handle request
        #recvData = message("code", "payload", "ID");
        recvData = pickle.loads(data)
        #recvData = data.decode('utf-8')
        msgCode = recvData.code
        msgPayload = recvData.payload
        msgSenderID = recvData.sender_ID
        

        #print("# RECEIVED MESSAGE from:"+str(client_address)+" With senderID:"+str(msgSenderID))
        #print("\nCode recieved: %s\n"%recvData.code)

        #Thread that tries to find the proof:
        t1 = threading.Thread(target=thread_find_proof)

        # send response to the client
        #print("[ RESPONSE to: ]")
        #print(client_address)
        #resp="message recieved"
        #with self.socket_lock:
        #    self.sock.sendto(resp.encode('utf-8'), client_address)
        #print("\n%s\n"%resp)

        if msgCode == "TOKEN":
            print("State Token Recieved")
            current_state=0
            self.TOKEN = True

            try:
                #Try to add block by sending "FIND NONCE"
                vote_data = q.get_nowait()
            except:
                next_id = (MY_ID + 1) % NUM_NODES
                self.transfer_token(((node_names[next_id], node_ports[next_id])))
            else:
                print("Proccessing Vote: name: %s vote: %s, email:%s",vote_data.name,vote_data.vote,vote_data.email)
                vote_block = Block(vote_data,local_blockchain.chain[-1].hash)
                payload = pickle.dumps(vote_block)
                for i in range(NUM_NODES):
                    if i != MY_ID:
                        self.send_request("FIND NONCE",payload,(node_names[i], node_ports[i]))

        elif msgCode == "FIND NONCE":#sent from root
            #print("State Find Nonce Value")
            current_state=1
            t1.start()
            

        elif msgCode == "NONCE FOUND":#send nonce to root
            #print("State send Nonce to other Nodes.")
            if current_state != 2:
                current_state=2
                current_block = pickle.loads(msgPayload)
                for i in range(NUM_NODES):
                    if i != MY_ID:
                        self.send_request("VALIDATE",msgPayload,(node_names[i], node_ports[i]))
                pass
        elif msgCode == "VALIDATE":#send nonce from root
            #print("State: Nonce Recieved Now Validate")
            current_state=3
            block = pickle.loads(msgPayload)
            #print("Recieved Block for Validation. nonce,hash,previous_hash: ",block.nonce," ",block.hash," ",block.previous_hash)
            #Block with Nonce Value Recieved
            local_blockchain.done_signal = 1
            if t1.is_alive():
                t1.join(0)
            #block.hash = block.generate_hash()
            local_blockchain.chain.append(block)
            is_valid = local_blockchain.validate_chain()
            payload = pickle.dumps(is_valid)
            local_blockchain.chain.pop(-1)
            self.send_request("VOTE",payload,(node_names[msgSenderID],node_ports[msgSenderID]))
            
                

        elif msgCode == "VOTE": # send vote to root
            #print("State: Vote Recieved")
            current_state=4
            #If True Vote, Increment vote_count
            vote = pickle.loads(msgPayload)
            if vote:
                print("Yes Vote Revieved")
                vote_count +=1
            
            #Check for Vote Success
            if vote_count > NUM_NODES/2:
                print("\n\n BLOCK VALIDATED ADDING TO CHAIN\n\n")
                local_blockchain.chain.append(current_block)
                payload = pickle.dumps(current_block)
                #If Success, Update chain.
                for i in range(NUM_NODES):
                    if i != MY_ID:
                        self.send_request("UPDATE CHAIN",payload,(node_names[i], node_ports[i]))
                
                #Block added to chain so transfer token.
                vote_count = 0
                next_id = (MY_ID + 1) % NUM_NODES
                self.TOKEN = False
                self.transfer_token(((node_names[next_id], node_ports[next_id])))
            if not(vote):
                print("No Vote Recieved")
                

            
        elif msgCode == "UPDATE CHAIN":#when 50% update chain and send to nodes
            #print("State: Updating Chain")
            current_state=5
            block = pickle.loads(msgPayload)
            #If new chain is the longest valid chain then replace it.
            if local_blockchain is None:
                local_blockchain=block
            else:
                local_blockchain.chain.append(block)
            print("Block chain updated: ")
            print("Length of chain: ",len(local_blockchain.chain))
            if len(local_blockchain.chain) >= 15:
                print("Max blocks reached.")
                exit(0)
                #local_blockchain.print_blocks()
                #print(local_blockchain.chain)

    def send_request(self, code,payload, dest_address):
        ''' Send message to other node '''
        #print("# Sending Msg to:")
        #print(dest_address)
        msg = pickle.dumps(message(code,payload,MY_ID))
        with self.socket_lock:
            self.sock.sendto(msg, dest_address)
        #print(f"#Sent: {code}")#, {payload}, {dest_address}
        #print(f"#Coded message: {msg}")
        #recvData, client_address = self.sock.recvfrom(MAX_VAL)
        #print("# Received Response: %s"%recvData)

    def transfer_token(self, dest_address):
        self.send_request("TOKEN", "", dest_address)
        self.TOKEN = False
        print("Transfered Token to next node")


    def wait_for_client(self):
        ''' Wait for clients and handle their requests '''

        try:
            flag = 0
            wait_flag = 1
            send_flag = 0

            while (flag == 0): # keep alive

                try: 
                    #if (self.TOKEN == True): # If node's turn to send data for verification
                    #    print("\nI HAVE THE TOKEN\n")
                    #    nextID = (MY_ID + 1) % NUM_NODES 

                        # Send token to next node.
                    #    self.transfer_token( (node_names[nextID], node_ports[nextID]) )
                    #    flag = 0

                    if (wait_flag == 1):
                        #print("# Waiting for Client Requests...")
                        data, client_address = self.sock.recvfrom(MAX_VAL)

                        c_thread = threading.Thread(target = self.handle_request,
                                            args = (data, client_address))
                        c_thread.daemon = True
                        c_thread.start()

                        time.sleep(2)

                    if (send_flag == 1):
                        sendData = 'Alex'
                        destAddr = node_names[1]
                        destPort = node_ports[1]
                        c_thread = threading.Thread(target = self.send_request, args = (sendData,(destAddr, destPort) ))
                        c_thread.daemon = True
                        c_thread.start()
                        time.sleep(2)
                        flag = 1


                except OSError as err:
                    self.printwt(err)

        except KeyboardInterrupt:
            self.shutdown_server()

def main():
    global local_blockchain
    ''' Create a UDP Server and handle multiple clients simultaneously '''
    udp_server_multi_client = UDPServerMultiClient(MY_NAME, MY_PORT)
    udp_server_multi_client.configure_server()

    if(MY_ID == 0):
        local_blockchain = Blockchain()
        if MY_ID == 0:
            local_blockchain.difficulty = int(input("What do you want the difficulty to be? "))
        for i in range(1,NUM_NODES):
            udp_server_multi_client.send_request("UPDATE CHAIN",pickle.dumps(local_blockchain),(node_names[i], node_ports[i]))
        udp_server_multi_client.transfer_token((node_names[1], node_ports[1]))

    cli_thread = threading.Thread(target = q.do_queue_loop)
    cli_thread.start()
    udp_server_multi_client.wait_for_client()

if __name__ == '__main__':
    main()
