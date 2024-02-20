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
from maker_bet import get_ty_num,cal_pro
import socket,sys
import random

def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
# 获取窗口句柄
    if handle == 0:
        return None
    else:
        return win32gui.GetWindowRect(handle), handle

def get_makers(num):
    a = random.uniform(1,3)
    if num == 0:
        pg.moveTo(240+x1,420+y1,duration=0.5)
        pg.dragTo(240+x1+a,420+y1+a,duration=0.2)
    elif num == 1:
        pg.moveTo(350+x1,420+y1,duration=0.6)
        pg.dragTo(350+x1+a,420+y1+a,duration=0.2)
    elif num == 2:
        pg.moveTo(460+x1,420+y1,duration=0.55)
        pg.dragTo(460+x1+a,420+y1+a,duration=0.2)
    elif num == 3:
        pg.moveTo(570+x1,420+y1,duration=0.45)
        pg.dragTo(570+x1+a,420+y1+a,duration=0.2)
    elif num == 4:
        pg.moveTo(690+x1,420+y1,duration=0.5)
        pg.dragTo(690+x1+a,420+y1+a,duration=0.25)

def get_bet(num):
    a = random.uniform(1,2)
    if num == 1:
        pg.moveTo(350+x1,420+y1,duration=0.5)
        pg.dragTo(350+x1+a,420+y1+a,duration=0.2)
    elif num == 2:
        pg.moveTo(460+x1,420+y1,duration=0.55)
        pg.dragTo(460+x1+a,420+y1+a,duration=0.25)
    elif num == 3:
        pg.moveTo(570+x1,420+y1,duration=0.5)
        pg.dragTo(570+x1+a,420+y1+a,duration=0.3)
    elif num == 4:
        pg.moveTo(690+x1,420+y1,duration=0.5)
        pg.dragTo(690+x1+a,420+y1+a,duration=0.2)

def quit_game():
    pg.moveTo(880+x1,70+y1,duration=1)
    pg.click()
    time.sleep(random.uniform(0.5,1))
    pg.moveTo(840+x1,190+y1,duration=1)
    pg.click()

def usual_action():
    i = 1
    while True:
        #坐下
        if pg.pixelMatchesColor(425+x1, 420+y1, (173, 130, 57), tolerance=10):
            time.sleep(random.uniform(0.1,0.6))
            pg.moveTo(450+x1,420+y1,duration=1)
            pg.dragTo(450+x1+random.uniform(0.1,0.6),420+y1+random.uniform(0.1,0.6),duration=0.6)

        #准备游戏
        elif pg.pixelMatchesColor(770+x1, 520+y1, (173, 130, 57), tolerance=10):
            time.sleep(random.uniform(0.5,1))
            img = ImageGrab.grab((x1, y1, x2, y2))  
            file = r"./1/{}.png".format(i)
            img.save(file)
            pg.moveTo(800+x1,500+y1,duration=1)
            pg.dragTo(800+x1+random.uniform(0.5,1),500+y1+random.uniform(0.5,1),duration=0.2)

        #亮牌
        elif pg.pixelMatchesColor(770+x1, 530+y1, (198, 40, 49), tolerance=10):
            time.sleep(random.uniform(0.5,2))
            pg.moveTo(820+x1,540+y1,duration=1)
            pg.dragTo(820+x1+random.uniform(0.5,2),540+y1+random.uniform(0.5,2),duration=0.2)

        #抢庄
        if pg.pixelMatchesColor(210+x1, 438+y1, (214, 146, 57), tolerance=10):
            time.sleep(random.uniform(0.5,1))
            img = ImageGrab.grab((x1, y1, x2, y2))  
            file = r"./tmp/{}.png".format(i)
            img.save(file)
            ty_card,my_cards = socket_client(reg_sock)
            ty_card_num = get_ty_num(my_cards,ty_card)
            m,b = cal_pro(my_cards,ty_card,ty_card_num)
            print('癞子数：%s'%ty_card_num,'抢庄：%s'%m,'下注：%s'%b)
            time.sleep(random.uniform(1,2))
            get_makers(m)

        #下注
        elif not pg.pixelMatchesColor(210+x1, 438+y1, (214, 146, 57), tolerance=10) and pg.pixelMatchesColor(330+x1, 436+y1, (107, 166, 220), tolerance=10):
            time.sleep(random.uniform(1.5,3))
            get_bet(b)

        i += 1


ADDR =('192.168.1.5',9999)
reg_sock = socket.socket()
reg_sock.connect(ADDR)
print('reg server connected success')
if not win32gui.FindWindow(0, '雷电模拟器-1'):          
        print('请先运行模拟器')
        # break
else:
    (x1, y1, x2, y2), handle1 = get_window_pos('雷电模拟器-1')
    print((x1, y1, x2, y2))     #(479, 231, 1477, 809)
    pg.press('down')
    win1 = win32gui.SetForegroundWindow(handle1)
    pg.press('enter')
usual_action()

    # while not pg.pixelMatchesColor(750+x1, 500+y1, (173, 135, 57), tolerance=10):
    #     pass
    #退出游戏
    # if pg.pixelMatchesColor(750+x1, 500+y1, (173, 135, 57), tolerance=10):
    #     time.sleep(2)
    #     quit_game()


# if not win32gui.FindWindow(0, '雷电模拟器-1'):          
#     print('请先运行模拟器')
#     # break
# else:
#     (x1, y1, x2, y2), handle1 = get_window_pos('雷电模拟器-1')
#     print((x1, y1, x2, y2))     #(580, 221, 1504, 777)
#     pg.press('down')
#     win1 = win32gui.SetForegroundWindow(handle1)

#     # 游戏截图获取按钮位置
#     for i in range(30):
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



















