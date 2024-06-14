import os
import platform
import subprocess
import threading
from datetime import datetime
from queue import Queue

print_lock = threading.Lock()
results = []

def check_host(ip, ping_command):
   response = os.popen(ping_command)
   for line in response.readlines():
      #print(line)
      reply = line.split()
      if len(reply) > 0 and reply[0] == 'Reply' and line.count("TTL"):
         with print_lock:
            results.append((ip, "Live"))

def threader():
   while True:
      ipPing = q.get()
      check_host(ipPing['ip'], ipPing['ping'])
      q.task_done()

net = "192.168.2.40"
a = '.'
net1 = net.split(a)

net2 = net1[0] + a + net1[1] + a + net1[2] + a
st1 = 1
en1 = 400
oper = platform.system()

if (oper == "Windows"):
   ping1 = "ping -n 1 "
elif (oper == "Linux"):
   ping1 = "ping -c 1 "
else :
   ping1 = "ping -c 1 "

t1 = datetime.now()
print ("Scanning in Progress:")

q = Queue()

for x in range(100):
   t = threading.Thread(target=threader)
   t.daemon = True
   t.start()

for ip in range(st1,en1):
   addr = net2 + str(ip)
   comm = ping1 + addr
   q.put({'ip' : addr, 'ping' : comm})

q.join()

# Print results in order
results.sort(key=lambda x: int(x[0].split('.')[-1]))
for result in results:
    print(result[0], "-->", result[1])
               
t2 = datetime.now()
total = t2 - t1
print ("Scanning completed in: ", total)