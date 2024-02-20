
import time
import socket,sys
import os
import threading
import struct
import hashlib
from PIL import Image, ImageGrab
from skimage import io
import matplotlib.pyplot as plt
import shutil

def socket_client(reg_sock):
    def data_deal(data):            #height = 578 , width = 962
        ty_card = None
        my_cards = []
        for i in data[0]:
            if 240/578 < float(i[1]) < 340/578 and 440/962 < float(i[0]) < 520/962:
                ty_card = data[1][data[0].index(i)]
            elif 270/962 < float(i[0]) < 630/962 and 450/578 < float(i[1]) < 570/578:
                my_cards.append(data[1][data[0].index(i)])
        # print(ty_card,my_cards)
        return ty_card,my_cards
    # ADDR =('192.168.1.5',9999)
    # reg_sock = socket.socket()
    # reg_sock.connect(ADDR)
    # print('reg server connected success')
    pic_path = './tmp/'
    if len(os.listdir(pic_path)) > 0:
        filelist = sorted(os.listdir(pic_path),key=lambda x:int(x[:-4]))
        filepath = pic_path + filelist[0]
        if os.path.isfile(filepath):
            fileinfo_size = struct.calcsize('64sl64s')
            with open(filepath, 'rb') as fp:
                data = fp.read()
            img_md5 = hashlib.md5(data).hexdigest()
            fhead = struct.pack('64sl64s', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size,img_md5.encode(encoding='utf-8'))
            reg_sock.send(fhead)
            reg_sock.sendall(data)
            print ('{0} file send over...'.format(filepath))
            res = reg_sock.recv(512).decode()
            if res == 'file send over!':
                res_size = reg_sock.recv(512).decode()
                reg_sock.sendall('准备接受数据'.encode('utf-8'))
                recv_size  = 0   
                recv_data = b''  
                while recv_size < int(res_size):  
                    res_data = reg_sock.recv(512)
                    recv_size += len(res_data)  
                    recv_data += res_data
                shutil.move(filepath,'./2/%s'%filelist[0])
                recv_data = eval(recv_data)
                print(recv_data)
                ty_card,my_cards = data_deal(recv_data)
        return ty_card,my_cards
        





# def show_img(name):
#     file = './{}.png'.format(name)
#     img = Image.open(file)
#     plt.imshow(img)
#     plt.show()



# show_img('16')




