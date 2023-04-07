import socket
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import matplotlib.pyplot as plt
import random
import string

#remove gaussian noise
#encrypted_audio_data=np.frombuffer(audio_data,dtype=np.float32)
#encrypted_audio_data-np.mean(encrypted_audio_data)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1",65432))
    audio_data=s.recv(1176000)
    AES_KEY = 'u7b0ZMchR8B0h1D1wQ4z6O1tpobHzFKj'
    AES_IV = 'r94bztbP2bVWsio2'
    decryptor = AES.new(AES_KEY.encode('utf-8'), AES.MODE_CFB, AES_IV.encode('utf-8'))
    audio_data_received=decryptor.decrypt(audio_data) 
    true_data=np.frombuffer(audio_data_received,dtype=np.float64)
    true_data=true_data.reshape((len(true_data)//2,2))
    #preprocessing
    #true_data=np.delete(true_data,np.where(true_data<np.finfo(dtype=np.float32).min))
    #true_data=np.delete(true_data,np.where(true_data>np.finfo(dtype=np.float32).max))
    #true_data=true_data[~np.isnan(true_data)]
    plt.figure()
    plt.plot(true_data)
    plt.title("Decrypted noisy data file")
    plt.savefig("Decrypted_file_with_attack.png")
    plt.show()
    print("Sample of Recieved file (in bytes) is: ",audio_data_received[:20])
    
    s.close()
