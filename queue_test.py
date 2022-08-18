import time
import random
import socket

hostname = socket.gethostname()
host = hostname.split('.')[0]
num = int(host.split('-')[1])

class Vote():
    def __init__(self,name,vote,email):
        self.name = name
        self.vote = vote
        self.email = email

names = ["Alex","Brian","Julia","John","Zach"]
emails = ["@gmail.com","@g.clemson.edu","@yahoo.com","@aol.com"]
votes = ["cpe","ece"]

queue = []

ece_count = 0
cpe_count = 0
for i in range(20):
    name = names[random.randint(0,len(names)-1)]
    email = name + emails[random.randint(0,len(emails)-1)]
    vote = votes[random.randint(0,len(votes)-1)]
    new_vote = Vote(name,vote,email)
    queue.append(new_vote)
    if vote == "cpe":
        cpe_count +=1
    else:
        ece_count += 1
    print(i,name,vote,email)
    time.sleep(.25)
    
print("ECE Count: ",ece_count)
print("CPE Count: ",cpe_count)
print(queue)
print(len(queue))
first_vote = queue.pop(0)
print(len(queue))
print(first_vote.name)
