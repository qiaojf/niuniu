import os
import matplotlib.pyplot as plt
import pyautogui as pg
import win32api
import win32con
import win32gui
from PIL import Image, ImageGrab
from skimage import io
import time
from nn_client import socket_client
import socket,sys
import random


class NnGame():
    def get_window_pos(self,name):
        name = name
        handle = win32gui.FindWindow(0, name)
        if handle == 0:
            return None
        else:
            return win32gui.GetWindowRect(handle), handle

    def get_makers(self,num,x1,y1):
        a = random.uniform(2,6)
        c = random.uniform(5,25)
        b = random.uniform(1,4)
        if num == 0:
            pg.moveTo(240+x1,420+y1,duration=random.uniform(0.4,0.8))
            pg.click(240+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        elif num == 1:
            pg.moveTo(350+x1,420+y1,duration=random.uniform(0.4,0.8))
            pg.dragTo(350+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        elif num == 2:
            pg.moveTo(460+x1,420+y1,duration=random.uniform(0.4,0.8))
            pg.dragTo(460+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        elif num == 3:
            pg.moveTo(570+x1,420+y1,duration=random.uniform(0.4,0.8))
            pg.dragTo(570+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        elif num == 4:
            pg.moveTo(690+x1,420+y1,duration=random.uniform(0.4,0.6))
            pg.dragTo(690+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        
    def get_bet(self,num,x1,y1):
        a = random.uniform(3,6)
        c = random.uniform(5,25)
        b = random.uniform(2,5)
        if num == 1:
            pg.moveTo(350+x1,420+y1,duration=random.uniform(0.4,0.8))
            pg.dragTo(350+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        elif num == 2:
            pg.moveTo(460+x1,420+y1,duration=random.uniform(0.4,0.8))
            pg.dragTo(460+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        elif num == 3:
            pg.moveTo(570+x1,420+y1,duration=random.uniform(0.4,0.8))
            pg.dragTo(570+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))
        elif num == 4:
            pg.moveTo(690+x1,420+y1,duration=random.uniform(0.4,0.6))
            pg.click(690+x1+a,420+y1+c+b,duration=random.uniform(0.3,0.5))

    # def quit_game(self):
    #     pg.moveTo(880+x1,70+y1,duration=1)
    #     pg.click()
    #     time.sleep(random.uniform(0.5,1))
    #     pg.moveTo(840+x1,190+y1,duration=1)
    #     pg.click()

    def usual_action(self,reg_sock,x1, y1, x2, y2,stradge_sock):
        i = 1
        while True:
            #坐下
            if pg.pixelMatchesColor(425+x1, 420+y1, (173, 130, 57), tolerance=10):          #[420,400],[425,420]
                time.sleep(0.3)
                pg.moveTo(450+x1,400+y1,duration=random.uniform(0.4,0.8))
                pg.dragTo(450+x1+random.uniform(1,5),400+y1+random.uniform(2,4),duration=random.uniform(0.3,0.5))
            #准备
            elif pg.pixelMatchesColor(770+x1, 520+y1, (173, 130, 57), tolerance=10):        #[770,520],[750,495]
                a = random.uniform(5,60)
                time.sleep(0.5)
                img = ImageGrab.grab((x1, y1, x2, y2))  
                file = r"./1/{}.png".format(i)
                img.save(file)
                pg.moveTo(800+x1+a,500+y1,duration=random.uniform(0.2,0.5))
                pg.dragTo(800+x1+a+random.uniform(2,6),500+y1+random.uniform(1,5),duration=0.3)
            #抢庄
            elif pg.pixelMatchesColor(200+x1, 435+y1, (214, 146, 57), tolerance=10):        #[207,435],[200,421],[200,435]
                time.sleep(0.5)
                img = ImageGrab.grab((x1, y1, x2, y2))  
                file = r"./tmp/{}.png".format(i)
                img.save(file)
                print('file saved!')
                m = socket_client(reg_sock,stradge_sock)
                print(m)
                time.sleep(0.3)
                self.get_makers(int(m),x1,y1)
                time.sleep(random.uniform(2,2.5))
                if pg.pixelMatchesColor(154+x1, 465+y1, (231, 51, 49), tolerance=10):
                    stradge_sock.sendall('抢庄成功'.encode('utf-8'))
                    print('抢庄成功')
                else:
                    stradge_sock.sendall('抢庄失败'.encode('utf-8'))
                    print('抢庄失败')
                b = stradge_sock.recv(512).decode()
                print(b)
            #下注
            elif pg.pixelMatchesColor(320+x1, 430+y1, (115, 182, 231), tolerance=10):
                time.sleep(0.1)
                if pg.pixelMatchesColor(200+x1, 435+y1, (52, 109, 132), tolerance=10):          #[330,434],[320,420]
                    time.sleep(0.3)
                    self.get_bet(int(b),x1,y1)
            #亮牌
            elif pg.pixelMatchesColor(770+x1, 530+y1, (198, 40, 49), tolerance=10):         #[780,530],[750,515]
                a = random.uniform(25,60)
                time.sleep(random.uniform(0.5,1))
                pg.moveTo(780+x1+a,520+y1,duration=0.55)
                pg.dragTo(780+x1+a+random.uniform(2,5),520+y1+random.uniform(1,6),duration=random.uniform(0.3,0.5))
            i += 1

    def run(self,name):
        ADDR =('10.21.4.186',9999)
        reg_sock = socket.socket()
        reg_sock.connect(ADDR)
        print('reg server connected success')
        ADDR1 =('10.21.4.186',8888)
        stradge_sock = socket.socket()
        stradge_sock.connect(ADDR1)
        print('stradge_sock server connected success')
        if not win32gui.FindWindow(0, name):          
            print('请先运行模拟器')
        else:
            (x1, y1, x2, y2), handle1 = self.get_window_pos(name)
            print((x1, y1, x2, y2))     #(479, 231, 1477, 809)
            pg.press('down')
            win1 = win32gui.SetForegroundWindow(handle1)
            pg.press('enter')
        self.usual_action(reg_sock,x1, y1, x2, y2,stradge_sock)


a = NnGame()
a.run('雷电模拟器-6')



# if not win32gui.FindWindow(0, '雷电模拟器-6'):          
#     print('请先运行模拟器')
#     # break
# else:
#     (x1, y1, x2, y2), handle1 = a.get_window_pos('雷电模拟器-6')
#     print((x1, y1, x2, y2))     #(580, 221, 1504, 777)
#     pg.press('down')
#     win1 = win32gui.SetForegroundWindow(handle1)
#     pg.press('enter')
#     # 游戏截图获取按钮位置
#     for i in range(50):
#         img = ImageGrab.grab((x1, y1, x2, y2))  
#         file = r"./tmp/{}.png".format(i)
#         img.save(file)
#         print(i)
#         time.sleep(1)

    #获取游戏结果
    # for i in range(7600,9000):
    #     if pg.pixelMatchesColor(15+x1, 350+y1, (125, 62, 7), tolerance=10) or pg.pixelMatchesColor(810+x1, 350+y1, (156, 85, 17), tolerance=10) or pg.pixelMatchesColor(720+x1, 140+y1, (239, 194, 66),tolerance=10):
    #         img = ImageGrab.grab((x1, y1, x2, y2))  
    #         file = r"./tmp/{}.png".format(i)
    #         img.save(file)
    #         print(i)
    #         time.sleep(8)
    #     time.sleep(1)



















