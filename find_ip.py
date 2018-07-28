import socket
import time
class find_ip():
 #socket.setdefaulttimeout(0.4)
 def func(self,bind_ip,bind_port,start_ip,connect_port):
  sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  sock.bind((bind_ip,bind_port))
  connect_ip=start_ip
  o=int(start_ip.split('.')[3])
  a,b,c=start_ip.split('.')[:3]
  before=time.time()
  for i in range(int(start_ip.split('.')[3]),256):
   try:
    sock.connect((connect_ip,connect_port))
    print(connect_ip+'\n')
    print(time.time()-before,' seconds\n')
    print((time.time()-before)/(i-o+1),' ip/second\n')
    return connect_ip
   except:
    connect_ip=a+'.'+b+'.'+c+'.'+str(i+1)
  if i==255:
   print('No Server Works Under '+start_ip)
   print((time.time()-before)/i,' ip/second')
   print(time.time()-before,' seconds\n')
   return 0
if __name__ =='__main__':
 finder=find_ip()
 bind_ip='192.168.1.100'
 bind_port=4500
 start_ip='192.168.1.100'
 connect_port=22
 finder.func(bind_ip,bind_port,start_ip,connect_port)
 
