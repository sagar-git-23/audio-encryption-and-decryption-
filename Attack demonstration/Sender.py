import socket
from scipy.io import wavfile 
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import string
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

fs,data = wavfile.read('audio.wav') #specify path

plt.figure()
plt.plot(data)
plt.title("Original audio plot")
plt.savefig("original_audio_plot.png")
plt.show()

with open('audio.wav', 'rb') as fd:
    contents = fd.read()
    
AES_KEY = 'u7b0ZMchR8B0h1D1wQ4z6O1tpobHzFKj'

AES_IV = 'r94bztbP2bVWsio2'

encryptor = AES.new(AES_KEY.encode("utf-8"), AES.MODE_CFB, AES_IV.encode("utf-8"))

padded_audio_data=pad(contents,AES.block_size)

encrypted_audio = encryptor.encrypt(padded_audio_data)

#time.sleep(5)

HOST='127.0.0.1'
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn,addr=s.accept()
    with conn:
        print(f"Connected by {addr}")
        conn.sendall(encrypted_audio)
        print("Encrypted original file (In bytes) is: ",encrypted_audio[:20])
        s.close()