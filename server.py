import socket
import time
import threading

class SSH_trans():

 def thread_func(self,sock_sshd,sock_ssh,alive_comfirm):
  try:
   sock_sshd.setblocking(0)
   sock_ssh.setblocking(0)
  except:
   print('cannot work')
   return b'cannot work'
  before1=time.time()
  after1=time.time()
  before2=time.time()
  after2=time.time()
  alive=1
  while 1:
   try:
    recvData_sshd=sock_sshd.recv(1024)
     #print(recvData_sshd)
    if(recvData_sshd!=alive_comfirm):
     sock_ssh.send(recvData_sshd)
      #print(recvData_sshd.decode('utf-8'))
    else:
    # (recvData_sshd==alive_comfirm):
     print('sshd trans client is aliving!')
    before1=time.time()
   except:
    recvData_sshd=b''
    after1=time.time()

   try:
    recvData_ssh=sock_ssh.recv(1024)
     #print(recvData_ssh)
    sock_sshd.send(recvData_ssh)
     #print(recvData_ssh.decode('utf-8'))
    before2=time.time()
   except:
    recvData_ssh=b''
    after2=time.time()

   if(after1-before1>15 and alive==1):
    alive=0
    time.sleep(0.1)
    sock_sshd.send(alive_comfirm)
    time.sleep(0.1)
   if(after1-before1>30):
    try:
     sock_sshd.close()
     sock_ssh.close()
     print('lost Client')
     return b'lost_Client'
    except:
     pass

   if(after2-before2>120):
    try:
     sock_sshd.close()
     sock_ssh.close()
     print('lost_SSH')
     return b'lost_SSH'
    except:
     pass


 def process_func(self,bind_ip,bind_port,alive_comfirm):
  sock_sshd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  sock_sshd.bind((bind_ip,bind_port[0]))
  sock_sshd.listen(53556)
  sock_ssh=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  sock_ssh.bind((bind_ip,bind_port[1]))
  sock_ssh.listen(53556)
  sshd=[]
  ssh=[]
  sock_sshd.setblocking(0)
  sock_ssh.setblocking(0)
  while 1:
   loop=1
   while loop==1:
    try:
     sshd.append(sock_sshd.accept()[0])
     print('sshd connected\n')
     ssh.append(sock_ssh.accept()[0])
     print('ssh connected\n')
     loop=0
    except:
     pass
    if(len(sshd)>16):
     del sshd[0]
    if(len(ssh)>16):
     del ssh[0]

   threading.Thread(target=self.thread_func,args=(sshd[-1],ssh[-1],alive_comfirm)).start()
   if(len(sshd)>64):
    del sshd[0]
   if(len(ssh)>64):
    del ssh[0]



if __name__ == '__main__':
 bind_ip='192.168.1.100'
 bind_port=(56850,56851)
 alive_comfirm=b'Are_You_Aliving?!'
 ss=SSH_trans()
 ss.process_func(bind_ip,bind_port,alive_comfirm)
