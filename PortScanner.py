import socket
import time
import threading
from queue import Queue

# Make sure that sockets timeout and print statements are appropriately locked
socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

# Get the network to be scanned
target = "192.168.2.40"
t_IP = socket.gethostbyname(target)
print ('Starting scan on host: ', t_IP)

# Takes in a port number and checks to see if it's open 
def portscan(port):
   # Create a socket to use to check a port
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   try:
      # See if the connection to the port works and print out the open port number
      con = s.connect((t_IP, port))
      with print_lock:
         print(port, 'is open')
      
      # Close the connection
      con.close()
   
   # If the port can't be connected to then move on to the next iteration
   except:
      pass

# Create threads to check port numbers
def threader():
   while True:
      # Get a port number from the queue and scan it
      port = q.get()
      portscan(port)
      q.task_done()

# Create a queue to store the port numbers
q = Queue()

# Get a start time for the runtime analysis
startTime = time.time()

# Make 100 threads to run through and check ports
for x in range(100):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()

# Add well known port numbers 1-1024 to the queue to be analyzed 
for port in range(0, 1024):
   q.put(port)
   
# Join the queue to prevent chasing with threads and the data
q.join()

# Display the time the port scan took
print('Time taken:', time.time() - startTime)