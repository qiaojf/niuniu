
import  select
import socket
import  queue
import random
import itertools
import time


user_num = 2
rand_cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
int_cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]
char_to_int = dict(zip(rand_cards, int_cards))
pokes = ['3d', '3c', '3h', '3s', '4d', '4h', '4s', '4c', '5s', '5h', 
    '5d', '5c', '6c', '6h', '6d', '6s', '7s', '7d', '7c', '7h', '8d', '8c',
        '8s', '8h', '9s', '9d', '9h', '9c', '10s', '10d', '10h', '10c', 'Js', 
        'Jc', 'Jd', 'Jh', 'Qh', 'Qc', 'Qs', 'Qd', 'Kd', 'Ks', 'Kc', 'Kh', 'As',
        'Ah', 'Ac', 'Ad', '2d', '2h', '2s', '2c', 'BJ', 'CJ']

def get_poke(ty_card,pokes):
    for i in pokes:
        if i[:-1] == str(ty_card):
            pokes[pokes.index(i)] = str(ty_card)
    if str(ty_card) == '10':
        pokes[28],pokes[29],pokes[30],pokes[31] = '10','10','10','10'
    return pokes

def get_ty_num(cards,ty_card):
    ty_card_num = cards.count(ty_card)
    for i in cards:
        if i in ['BJ','CJ']:
            ty_card_num += 1
    return ty_card_num

def candy_poke(data_list,pokes):
    candy_cards = get_poke(data_list[0].queue[0][0],pokes)
    for i in data_list:
        for j in i.queue[0][1]:
            candy_cards.remove(j)
    left_tycard_num = get_ty_num(candy_cards,str(data_list[0].queue[0][0]))
    del_list = []
    for i in range(len(candy_cards)):
        if candy_cards[i] in ['BJ','CJ',str(data_list[0].queue[0][0])]:
            del_list.append(candy_cards[i])
    for i in del_list:
        candy_cards.remove(i)
    return candy_cards,left_tycard_num

def cal_pro(cards,ty_card,ty_card_num,candy_cards,left_tycard_num):
    print(cards)
    if 'BJ' in cards:
        cards.remove('BJ')
    if 'CJ' in cards:
        cards.remove('CJ')
    if ty_card in cards:
        while ty_card in cards:
            cards.remove(ty_card)
    cards_char = [x[:-1] for x in cards]
    cards_char = sorted(cards_char, key=lambda x:rand_cards.index(x))
    cards_int = [char_to_int[x] for x in cards_char]
    shunzi4_list = [['2','3','4','5'],['3','4','5','6'],['4','5','6','7'],['5','6','7','8'],['6','7','8','9'],['7','8','9','10'],
                ['8','9','10','J'],['9','10','J','Q']]
    print(cards_char)
    # user_num = q.qsize()
    if ty_card_num == 0:
        #同花顺 例如：'2s','3s','4s','5s' ,期望为6/50*18+6/50*14+8/50*32-30/50*10=84/50
        if cards_char in shunzi4_list and ty_card not in [rand_cards[rand_cards.index(cards_char[0])-1],rand_cards[rand_cards.index(cards_char[-1])+1]] and cards[0][-1] == cards[1][-1] == cards[2][-1] == cards[3][-1]: 
            tonghua_num,shunzi_num,tonghuashun_num = 0,0,0
            for i in candy_cards:
                if i[-1] == cards[0][-1] and i[:-1] not in [rand_cards[rand_cards.index(cards_char[0])-1],rand_cards[rand_cards.index(cards_char[-1])+1]]:
                    tonghua_num += 1
                elif i[-1] != cards[0][-1] and i[:-1] in [rand_cards[rand_cards.index(cards_char[0])-1],rand_cards[rand_cards.index(cards_char[-1])+1]]:
                    shunzi_num += 1
                elif i[-1] == cards[0][-1] and i[:-1] in [rand_cards[rand_cards.index(cards_char[0])-1],rand_cards[rand_cards.index(cards_char[-1])+1]]:
                    tonghuashun_num += 1
            ep = tonghua_num*18+shunzi_num*14+(tonghuashun_num+left_tycard_num)*32-(54-user_num*4-tonghua_num-shunzi_num-tonghuashun_num-left_tycard_num)*10
            if ep > 0:
                mag = 40
            else:
                mag = 0
        #有两对且相加和为10，例如：3，3，7，7，期望为16/50*12+10/50*20-24/50*10=152/50
        elif len(list(set(cards_int))) == 2 and list(set(cards_int))[0] + list(set(cards_int))[1] == 10 and cards_char.count(cards_char[0]) == 2:
            biyi_num,hulu_num = 0,0
            for i in candy_cards:
                if i[:-1] in cards_char:
                    hulu_num += 1
                elif i[:-1] in ['10','J','Q','K']:
                    biyi_num += 1
            ep = biyi_num*12+(hulu_num+left_tycard_num)*20-(54-user_num*4-biyi_num-hulu_num-left_tycard_num)*10
            if ep > 0:
                mag = 20
            else:
                mag = 0
        #四张牌是10,J,Q,K          期望为12/50*16+4/50*14+10/50*26-24/50*10=268/50
        elif cards_char == ['10','J','Q','K']:
            wuhua_num,shunzi_num,tianlong_num = 0,0,0
            for i in candy_cards:
                if i[:-1] in ['10','J','Q','K']:
                    wuhua_num += 1
                elif i[:-1] == '9':
                    shunzi_num += 1
                elif i[:-1] == 'A':
                    tianlong_num += 1
            ep = wuhua_num*16+shunzi_num*14+(tianlong_num+left_tycard_num)*26-(54-user_num*4-wuhua_num-shunzi_num-tianlong_num-left_tycard_num)*10
            if ep > 0:
                mag = 30
            else:
                mag = 0
        #四张牌都大于等于10，例如：10，J,J,J 期望为8/50*16+3/50*20+7/50*22-32/50*10=22/50
        elif all(x in ['10','J','Q','K'] for x in cards_char) and len(list(set(cards_char))) ==2 and ty_card not in ['10','J','Q','K']:
            wuhua_num,hulu_num = 0,0
            for i in candy_cards:
                if i[:-1] not in list(set(cards_char)) and i[:-1] in ['10','J','Q','K']:
                    wuhua_num += 1
                elif i[:-1] in list(set(cards_char)):
                    hulu_num += 1
            ep = wuhua_num*16+(hulu_num+left_tycard_num)*20-(54-user_num*4-wuhua_num-hulu_num-left_tycard_num)*10
            if ep > 0:
                mag = 30
            else:
                mag = 0
        #四张牌点数相同,例如：4，4，4，4
        elif len(list(set(cards_char))) == 1:
            mag = 40
        #四张牌都小于等于5，例如：1，2，3，1,期望为14/50*28-36/50*10=32/50
        elif cards_int[0] + cards_int[1] + cards_int[2] + cards_int[3] <= 7:
            wuxiao_num = 0
            for i in candy_cards:
                if i[:-1] in ['A','2','3','4','5'] and cards_int[0] + cards_int[1] + cards_int[2] + cards_int[3] + char_to_int[i[:-1]] <= 10:
                    wuxiao_num += 1
            ep = (wuxiao_num+left_tycard_num)*28-(54-user_num*4-wuxiao_num-left_tycard_num)*10
            if ep > 0:
                mag = 5
            else:
                mag =0
        else:
            mag = 0
    elif ty_card_num == 1:
        #癞子是K，有Q,例如：4，6，Q
        if ty_card == 'K' and 'Q' in cards_char:
            niuniu_num = 0
            #前两张牌都小于10，且和也不等于10，例如：7，8，Q  期望为12/50*10+11/50*10+5/50*10-22/50*10=60/50
            if cards_int[0] < 10 and cards_int[1] < 10 and cards_int[0] + cards_int[1] != 10:
                for i in candy_cards:
                    if i[:-1] in ['10','J','Q','K']:
                        niuniu_num += 1
                    elif char_to_int[i[:-1]] in [10-cards_int[0],10-cards_int[1],10-cards_int[0]-cards_int[1],20-cards_int[0]-cards_int[1]]:
                        niuniu_num += 1
                ep = (niuniu_num+left_tycard_num)*10 - (54-niuniu_num-left_tycard_num)*10
                if ep > 0:
                    mag = 5
                else:
                    mag = 0
            else:
                mag = 10
        #有K，例如:3,J,K
        elif 'K' in cards_char:
            niuniu_num = 0
            #前两张牌都小于10，且和也不等于10，例如：7，8，K
            if cards_int[0] < 10 and cards_int[1] < 10 and cards_int[0] + cards_int[1] != 10:
                for i in candy_cards:
                    if i[:-1] in ['10','J','Q','K']:
                        niuniu_num += 1
                    elif char_to_int[i[:-1]] in [10-cards_int[0],10-cards_int[1],10-cards_int[0]-cards_int[1],20-cards_int[0]-cards_int[1]]:
                        niuniu_num += 1
                ep = (niuniu_num+left_tycard_num)*10 - (54-niuniu_num-left_tycard_num)*10
                if ep > 0:
                    mag = 5
                else:
                    mag = 0
            else:
                mag = 10
        #有一对，且有两张牌和为10，例如：4，6，4 ，期望为16/50*12+7/50*22+3/50*20-24/50*10=166/50
        elif len(list(set(cards_int))) == 2 and list(set(cards_int))[0] + list(set(cards_int))[1] == 10:
            biyi_num,hulu_num = 0,0
            for i in candy_cards:
                if i[:-1] in ['10','J','Q','K']:
                    biyi_num += 1
                elif i[:-1] in list(set(cards_char)):
                    hulu_num += 1
            ep = biyi_num*12+(hulu_num+left_tycard_num)*20-(54-user_num*4-biyi_num-hulu_num-left_tycard_num)*10
            if ep > 0:
                mag = 20
            else:
                mag = 0
        #同花且是顺子中的三张,例如：3d，5d，6d，期望为9/50*14+6/50*18+8/50*32-28/50*10=198/50
        elif cards[0][-1] == cards[1][-1] and cards[0][-1] == cards[2][-1] and (int(rand_cards.index(cards_char[2])) - int(rand_cards.index(cards_char[0]))) <= 3 and len(list(set(cards_char))) == 3:
            mag = 40
        #三张牌是10的倍数，且有一对，例如：7，7，6或者2，4，4，期望为3/50*20+7/50*22+16/50*12-24/50*10=166/50
        elif len(list(set(cards_int))) == 2 and (cards_int[0] + cards_int[1] + cards_int[2] in [10,20]):
            biyi_num,hulu_num = 0,0
            for i in candy_cards:
                if i[:-1] in ['10','J','Q','K']:
                    biyi_num += 1
                elif i[:-1] in list(set(cards_char)):
                    hulu_num += 1
            ep = biyi_num*12+(hulu_num+left_tycard_num)*20-(54-user_num*4-biyi_num-hulu_num-left_tycard_num)*10
            if ep > 0:
                mag = 20
            else:
                mag = 0
        #三张点数相同，例如：5，5，5
        elif len(list(set(cards_char))) == 1:
            mag = 40
        #三张花牌且不相等,例如：J,Q,K，期望为9/50*16+4/50*14+13/50*26-24/50*10=298/50
        elif len(list(set(cards_char))) == 3 and all(x in ['10','J','Q','K'] for x in cards_char):
            wuhua_num,shunzi_num,tianlong_num = 0,0,0
            for i in candy_cards:
                if i[:-1] in list(set(cards_char)):
                    wuhua_num += 1
                elif i[:-1] == '9':
                    shunzi_num += 1
                elif i[:-1] == 'A':
                    tianlong_num += 1
            ep = wuhua_num*16+shunzi_num*14+(tianlong_num+left_tycard_num)*26-(50-user_num*4-wuhua_num-shunzi_num-tianlong_num-left_tycard_num)*10
            if ep > 0:
                mag = 30
            else:
                mag = 0
        #两张牌或三张牌和是10的倍数，例如1,2,7或1，3，7或2，5，8或4，6，9或2，J，Q
        elif (cards_int[0] + cards_int[1] == 10 or cards_int[0] + cards_int[2] == 10 or cards_int[1] + cards_int[2] in [10,20] or cards_int[0] + cards_int[1] + cards_int[2] in [10,20]) and cards_char[-1] != 'K':
            mag = 0
        #三张牌小于等于5，且不相等，例如1，3，4  期望为13/50*24-37/50*10+3/50*28 = 26/50
        elif len(list(set(cards_char))) == 3 and all(x in ['A','2','3','4','5'] for x in cards_char) and ty_card not in ['A','2','3','4','5']:
            dilong_num,shunzi_num = 0,0
            for i in candy_cards:
                if i[:-1] in ['A','2','3','4','5'] and i[:-1] not in list(set(cards_char)):
                    dilong_num += 1
                elif i[:-1] == '6' and 'A' not in list(set(cards_char)):
                    shunzi_num +=1
            ep = shunzi_num*14+(dilong_num+left_tycard_num)*24-(54-user_num*4-shunzi_num-dilong_num-left_tycard_num)*10
            if ep > 0:
                mag = 5
            else:
                mag = 0
        #三张牌小于等于5，和小于7，例如：1，1，4 期望为14/50*28-36/50*10=32/50
        elif cards_int[0] + cards_int[1] + cards_int[2] < 7:
            wuxiao_num = 0
            for i in candy_cards:
                if i[:-1] in ['A','2','3','4','5'] and cards_int[0] + cards_int[1] + cards_int[2] + char_to_int[i[:-1]] <= 9:
                    wuxiao_num += 1
            ep = (wuxiao_num+left_tycard_num)*28-(54-user_num*4-wuxiao_num-left_tycard_num)*10
            if ep > 0:
                mag = 5
            else:
                mag = 0
        #三张花牌，且有一对，例如：10，J,J,期望为3/50*20+7/50*22+8/50*16-32/50*10=22/50
        elif len(list(set(cards_char))) == 2 and all(x in ['10','J','Q','K'] for x in cards_char) and ty_card not in ['10','J','Q','K']:
            wuhua_num,hulu_num = 0,0
            for i in candy_cards:
                if i[:-1] in list(set(cards_char)):
                    hulu_num += 1
                elif i[:-1] in ['10','J','Q','K'] and i[:-1] not in list(set(cards_char)):
                    wuhua_num += 1
            ep = wuhua_num*16+(hulu_num+left_tycard_num)*20-(54-user_num*4-wuhua_num-hulu_num-left_tycard_num)*10
            if ep > 0:
                mag = 30
            else:
                mag = 0
        else:
            mag = 0
    elif ty_card_num == 2:
        if ty_card == 'K' and 'Q' in cards_char: #癞子是K，有Q
            mag = 10
        elif 'K' in cards_char:        #有K
            mag = 10 
        elif int(rand_cards.index(cards_char[1])) - int(rand_cards.index(cards_char[0])) <= 3:                    #顺子或炸弹，例如：5，8,期望为16/50*14+10/50*22-24/50*10=204/50
            mag = 20
        elif cards[0][-1] == cards[1][-1] and int(rand_cards.index(cards_char[1])) - int(rand_cards.index(cards_char[0])) <= 4: #同花顺，例如：5h,9h
            mag = 40
        elif cards_int[0] + cards_int[1] == 10:          #比翼,炸弹，例如：3，7，期望为10/50*22+16/50*12-24/50*10=172/50
            mag = 20
        elif cards[0][-1] == cards[1][-1]:   #同花,例如：3s,8s 期望为10/50*18+10/50*22-30/50*10=100/50
            mag = 30 
        elif cards_int[1] - cards_int[0] >= 5 and cards[0][-1] != cards[1][-1]:         #'2s' ,'9c'
            mag = 5
        else:           
            mag = 10
    elif ty_card_num == 3:
        mag = 40
    elif ty_card_num == 4:
        mag = 40
    return mag

def make_decision(stradge_list):
    decision = {}
    add = [x[0] for x in stradge_list]
    mag = [x[1] for x in stradge_list]
    for i in add:
        decision[i] = queue.Queue()
        if 40 in mag:
            if mag[add.index(i)] == 40:
                decision[i].put(4)
            else:
                decision[i].put(0)
        elif 40 not in mag and 30 in mag:
            if mag[add.index(i)] == 30:
                decision[i].put(4)
            else:
                decision[i].put(0)
        elif 40 not in mag and 30 not in mag and 20 in mag:
            if mag[add.index(i)] == 20:
                decision[i].put(4)
            else:
                decision[i].put(0)
        elif 40 not in mag and 30 not in mag and 20 not in mag and 10 in mag:
            if mag[add.index(i)] == 10:
                decision[i].put(4)
            else:
                decision[i].put(0)
        else:
            decision[i].put(0)
    return decision

def make_bets(res_list,msg_list):
    mag = [x[1] for x in res_list]
    bet = {}
    address = [x[0] for x in res_list]
    res = [x.queue[0] for x in msg_list]
    if '抢庄成功' in res:
        for i in address:
            bet[i] = queue.Queue()
            bet[i].put(1)
    else:
        for i in address:
            bet[i] = queue.Queue()
            if mag[address.index(i)] in [5,10,20,30,40]:
                bet[i].put(4)
            else:
                bet[i].put(1)
    return bet

def get_mark(list):
    mark = False
    for i in list:
        if i.empty():
            mark = True
        else:
            pass
    return mark

#创建socket连接
server = socket.socket()
server.bind(('10.21.4.186',8888))
server.listen(100)
server.setblocking(False)
mes_dic = {}
bet_dic = {}

inputs = [server,]
outputs = []

while True:
    readable,writeable,exceptional = select.select(inputs,outputs,inputs)
    for r in  readable:
        if r is server:         #代表来了一个新连接
            conn,addr = server.accept()
            inputs.append(conn)
            mes_dic[conn] = queue.Queue()
            bet_dic[conn] = queue.Queue()
        else:           #代表现有连接发送数据过来
            data = r.recv(512).decode()
            try:
                data = eval(data)
            except NameError:
                bet_dic[r].put(data)
            else:
                mes_dic[r].put(data)

    #要返回给客户端的连接列表
    for w in writeable:
        if not mark1:
            data_to_client = decision[w].get()
            w.sendall(str(data_to_client).encode('utf-8'))
        elif not mark2:
            send_data = bet[w].get()
            w.sendall(str(send_data).encode('utf-8'))
        outputs.remove(w)

    if len(mes_dic) == user_num:
        data_list = list(mes_dic.values())      #数据队列列表
        mark1 = get_mark(data_list)
        if not mark1:
            addr_list = list(mes_dic.keys())    #连接对象列表
            for x in addr_list:
                outputs.append(x)
            res_list = []
            candy_cards,left_tycard_num = candy_poke(data_list,pokes)
            for d in data_list:
                data_tuple = d.queue
                ty_card_num = get_ty_num(d.queue[0][1],str(d.queue[0][0]))
                mag = cal_pro(d.queue[0][1],str(d.queue[0][0]),ty_card_num,candy_cards,left_tycard_num)
                res_list.append((addr_list[data_list.index(d)],mag))
                d.get()
            decision = make_decision(res_list)
            pokes = ['3d', '3c', '3h', '3s', '4d', '4h', '4s', '4c', '5s', '5h', 
            '5d', '5c', '6c', '6h', '6d', '6s', '7s', '7d', '7c', '7h', '8d', '8c',
            '8s', '8h', '9s', '9d', '9h', '9c', '10s', '10d', '10h', '10c', 'Js', 
            'Jc', 'Jd', 'Jh', 'Qh', 'Qc', 'Qs', 'Qd', 'Kd', 'Ks', 'Kc', 'Kh', 'As',
            'Ah', 'Ac', 'Ad', '2d', '2h', '2s', '2c', 'BJ', 'CJ']

    if len(bet_dic) == user_num:
        msg_list = list(bet_dic.values())      #数据对象列表
        mark2 = get_mark(msg_list)
        if not mark2:
            addr_list = list(bet_dic.keys())    #地址列表
            for x in addr_list:
                outputs.append(x)
            bet = make_bets(res_list,msg_list)
            for m in msg_list:
                m.get()

    for e in exceptional:
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)
        del  mes_dic[e]









































