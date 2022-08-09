import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def reci(c):
    while True:
        data = c.recv(2048)
        if len(data) !=0:
            print(data.decode("ascii"))

def server():
    port = 4545
    ip = "127.0.0.1"
    pub_key = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxBPyXZFuJHcncVKMh58n
    1caF5LO1/BOCwYRCo4f4cxR7u17JErHa8Rx8ydtAdmBg6TIuhlN7USrhPyv0hppY
    PoApAAgLYt7hu2Lm2qUtUlZkvA8GLn81AhHi/RIejFPTb/IqW5a+dGtXtY/TTCpf
    Ee4tqDFBOQdz85VcsAwKoliqr4mpb8Z/tJ6MH+/LZTUPqtJ5PTdm8RXLgmpjhh1I
    J4sz7np7Su6FFqao6Sgwh3k+JIelg8/K7Txwd2Kv9AQBoamm2Q4ho+Sf1/d/7cjI
    2I8sazbyWTKyValU6q62ujUfX92fBOVxB0MdTYKkYPnXHSpBfWqKZXPrU/LeLwOh
    cwIDAQAB
    -----END PUBLIC KEY-----"""
    pub_key=pub_key.encode("ascii")
    pupkey=RSA.importKey(pub_key)
    c = PKCS1_OAEP.new(pupkey)
    key=input("Enter Your Key:  ")
    encrypted_key = c.encrypt(key.encode("ascii"))
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setblocking(1)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((ip,port))
        s.listen(1)
        c , add = s.accept()
        print("connection from {0}:{1}".format(add[0],add[1]))
        c.send(encrypted_key)
        t= threading.Thread(target=reci,args=(c,))
        t.start()
        while True:
            command=input(" Enter Your Command >> ")
            c.send(command.encode("ascii"))
    except socket.error as e:
        print(e)
        s.close()

server()
