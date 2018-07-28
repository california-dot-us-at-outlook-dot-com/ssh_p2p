import socket 
import threading
import time

class SSH_trans():
 waitingClient=0 
 lock=threading.Lock()
 def thread_func(self,server_ip,server_port,SSH_ip,SSH_port,sock_toServer,sock_to22,alive_comfirm):
  try:
   sock_to22.connect((SSH_ip,SSH_port))
   sock_toServer.connect((server_ip,server_port))
  except:
   self.lock.acquire()
   self.waitingClient=self.waitingClient-1
   self.lock.release()
   print('Cannot Connect Server!')
   return b'Cannot Connect Server'
   

  before1=time.time()
  after1=time.time()
  before2=time.time()
  after2=time.time()
  once_work=0
  alive=1
  while 1:
   sock_to22.setblocking(0)
   sock_toServer.setblocking(0)
  
   try:
    recvData_S=sock_toServer.recv(1024)
     #print(recvData_S)

    if(recvData_S!=alive_comfirm):
     sock_to22.send(recvData_S)
     if(once_work==0):
      once_work=1
      self.lock.acquire()
      self.waitingClient=self.waitingClient-1
      self.lock.release()
    elif(recvData_S==alive_comfirm):
     print('Server is aliving!')
    before1=time.time()
   except:
    recvData_S=b''
    after1=time.time()
 
   try:
    recvData_22=sock_to22.recv(1024)
     #print(recvData_22)
    sock_toServer.send(recvData_22)
    before2=time.time()
   except:
    recvData_22=b''
    after2=time.time()
 
   if(after1-before1>15 and alive==1):
    alive=0
    time.sleep(0.1)
    sock_toServer.send(alive_comfirm)
    time.sleep(0.1)
   if(after1-before1>30):
    try:
     sock_to22.close()
     sock_toServer.close()
     if once_work==0:
      self.lock.acquire()
      self.waitingClient=self.waitingClient-1
      self.lock.release()
     print('lost_Server')
     return b'lost_Server'
    except:
     pass

   if(after2-before2>120):
    try:
     sock_to22.close()
     sock_toServer.close()
     if once_work==0:
      self.lock.acquire()
      self.waitingClient=self.waitingClient-1
      self.lock.release()
     print('lost_SSH')
     return b'lost_SSH'
    except:
     pass
 


 def findFreePort(self,bind_ip,start_ip):
  sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  for i in range(start_ip,65536):
   try:
    sock.bind((bind_ip,i))
    return sock,i
   except:
    i=i+1
  print('No port to bind')
  return b'No port to bind'
   
 
 def process_func(self,server_ip,server_port,bind_ip,bind_port,SSH_ip,SSH_port,alive_comfirm):
  self.waitingClient=0
  while 1:
   if(self.waitingClient==0):
    try:
     sock1,start_port=self.findFreePort(bind_ip,bind_port)
     sock2,start_port=self.findFreePort(bind_ip,start_port)
     threading.Thread(target=self.thread_func,args=(server_ip,server_port,SSH_ip,SSH_port,sock1,sock2,alive_comfirm)).start()
     self.lock.acquire()
     self.waitingClient=1+self.waitingClient
     self.lock.release()
    except:
     pass

 def initial_func(self):
  server_ip='192.168.1.100'
  server_port=56811
  bind_ip='127.0.0.1'
  bind_port=1200
  SSH_ip='127.0.0.1'
  SSH_port=22
  alive_comfirm=b'Are_You_Aliving?!'
  return server_ip,server_port,bind_ip,bind_port,SSH_ip,SSH_port,alive_comfirm

if __name__ == '__main__':
 server_ip='192.168.1.100'
 server_port=56856
 bind_ip='192.168.1.100'
 bind_port=1200
 SSH_ip='192.168.1.100'
 SSH_port=22
 alive_comfirm=b'Are_You_Aliving?!'

 ss=SSH_trans()
 ss.process_func(server_ip,server_port,bind_ip,bind_port,SSH_ip,SSH_port,alive_comfirm)
