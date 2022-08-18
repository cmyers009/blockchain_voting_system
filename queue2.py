from voteInfo import voteInfo
#from get_vote import get_vote
from queue import Queue
import time
import random

names = ["Alex","Brian","Julia","John","Zach"]
emails = ["@gmail.com","@g.clemson.edu","@yahoo.com","@aol.com"]
votes = ["cpe","ece"]

def do_queue_loop(self,verbose=True):
    #Queue timing variables
    Tic = None
    Toc = None

    #Local Measurement variables
    total_interarrival_time = 0

    #Input/Arrival Loop
    while True:
        #vote = get_vote()
        name = names[random.randint(0,len(names)-1)]
        email = name + emails[random.randint(0,len(emails)-1)]
        vote = votes[random.randint(0,len(votes)-1)]
        voteObj = voteInfo(name,vote,email)


        print(name,vote,email)
        time.sleep(random.randint(0,30))

        if voteObj:
            try:
                self.put(voteObj)
            except:
                print("Could not add item to queue")
            else:
                if Tic is not None:
                    Toc = time.perf_counter()
                    interarrival_time = Toc - Tic
                    total_interarrival_time += interarrival_time
                    if self.arrival_count > 1:
                        self.avg_interarrival_time = total_interarrival_time / (self.arrival_count - 1)

                    if(verbose):
                        print(f"Recent interarrival time is {interarrival_time: 0.4f} seconds")
                
                Tic = time.perf_counter()
                self.arrival_count += 1

        if(verbose):
            print(f"Number of vote submissions/arrivals is: {self.arrival_count}")
            print(f"Total currently in queue: {self.qsize()}")
            print(f"Average inerarrival time: {self.avg_interarrival_time}\n")

#deprecated
@DeprecationWarning
def do_server(self,verbose):
    server_vote = None
    #Server timing variables
    Tic = None
    Toc = None

    #local measurement vars
    service_time = float('inf')
    total_service_time = float('inf')

    #Populate server from queue
    #Don't need to check if queue is empty - get() is blocking
    #but get_nowait is not blocking will raise exception if queue is empty
    if server_vote is None:
        try:
            server_vote = self.get_nowait()
        except:
            if(verbose):
                print("Could not retrieve item from queue")
            return None
    
    #Try to add vote to blockchain
    if server_vote is not None:
        #self.attempted_submissions += 1
        #Tic = time.perf_counter()
        #local_chain.add_block(server_vote)
        #if local_chain.validate_chain()
        #Toc = time.perf_counter()
        #if successful
        #service_time = Toc - Tic
        #total_service_time += service_time
        #self.avg_service_time = total_service_time / self.confirmed_submissions

        return server_vote

Queue.arrival_count = 0
Queue.avg_interarrival_time = float('inf')
Queue.attempted_submissions = 0
Queue.confirmed_submissions = 0
Queue.avg_service_time = float('inf')
Queue.do_queue_loop = do_queue_loop
Queue.do_server = do_server