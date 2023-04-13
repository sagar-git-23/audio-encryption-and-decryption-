import socket
import numpy as np
from scipy.io import wavfile 
import random
import matplotlib.pyplot as plt
from Crypto.Util.Padding import pad,unpad
from Crypto.Cipher import AES

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1",65432))
    encrypted_audio=s.recv(294736)
    AES_KEY = 'u7b0ZMchR8B0h1D1wQ4z6O1tpobHzFKj'
    AES_IV = 'r94bztbP2bVWsio2'
    #decrypt the encrypted file and add noise to it
    decryptor = AES.new(AES_KEY.encode('utf-8'), AES.MODE_CFB, AES_IV.encode('utf-8'))
    decrypted_audio = decryptor.decrypt(encrypted_audio)
    #remove the padding
    decrypted_audio=unpad(decrypted_audio,AES.block_size)
    with open("decrypt.wav","wb") as f:
        f.write(decrypted_audio)
    fs,data=wavfile.read("decrypt.wav")
    # add gaussian noise
    sample_noise=np.random.randn(len(data)*2).reshape(data.shape)
    noisy_audio_data=data+sample_noise
    plt.plot(noisy_audio_data)
    plt.title("Original file with noise")
    plt.show()
    encryptor = AES.new(AES_KEY.encode('utf-8'), AES.MODE_CFB, AES_IV.encode('utf-8'))
    #encrypt the noise data and send to the reciver
    encrypted_noise_audio=encryptor.encrypt(bytes(noisy_audio_data))
    print("Encrypted noisy original file (in bytes) is: ",encrypted_noise_audio[:20])    
    s.close()


if encrypted_audio:
    HOST='127.0.0.1'
    PORT=65432

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()
        conn,addr=s.accept()
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(encrypted_noise_audio)
            s.close() 
            
     