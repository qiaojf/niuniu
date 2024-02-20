
import random
import itertools
import time
from nn_client import socket_client


rand_cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
int_cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]
char_to_int = dict(zip(rand_cards, int_cards))
pokes = ['3d', '3c', '3h', '3s', '4d', '4h', '4s', '4c', '5s', '5h', 
    '5d', '5c', '6c', '6h', '6d', '6s', '7s', '7d', '7c', '7h', '8d', '8c',
        '8s', '8h', '9s', '9d', '9h', '9c', '10s', '10d', '10h', '10c', 'Js', 
        'Jc', 'Jd', 'Jh', 'Qh', 'Qc', 'Qs', 'Qd', 'Kd', 'Ks', 'Kc', 'Kh', 'As',
        'Ah', 'Ac', 'Ad', '2d', '2h', '2s', '2c', 'BJ', 'CJ']
p_list = list(itertools.combinations(pokes,5))
no_king_list = [x for x in p_list if ('BJ' or 'CJ') not in x]
shunzi_list = [['A','2','3','4','5'],['2','3','4','5','6'],['3','4','5','6','7'],['4','5','6','7','8'],['5','6','7','8','9'],['6','7','8','9','10'],
            ['7','8','9','10','J'],['8','9','10','J','Q'],['9','10','J','Q','K'],['10','J','Q','K','A']]
def get_poke(rand_cards,pokes):
    ty_card = random.choice(rand_cards)
    print(ty_card)
    for i in pokes:
        if i[0] == ty_card:
            pokes[pokes.index(i)] = ty_card
    if ty_card == '10':
        pokes[28],pokes[29],pokes[30],pokes[31] = '10','10','10','10'
    return pokes,ty_card

def send_cards(pokes):
    user1_cards = random.sample(pokes,4)
    for i in user1_cards:
        pokes.remove(i)
    user2_cards = random.sample(pokes,4)
    for i in user2_cards:
        pokes.remove(i)
    user3_cards = random.sample(pokes,4)
    for i in user3_cards:
        pokes.remove(i)
    user4_cards = random.sample(pokes,4)
    for i in user4_cards:
        pokes.remove(i)
    user5_cards = random.sample(pokes,4)
    for i in user5_cards:
        pokes.remove(i)
    user6_cards = random.sample(pokes,4)
    for i in user6_cards:
        pokes.remove(i)
    user7_cards = random.sample(pokes,4)
    for i in user7_cards:
        pokes.remove(i)
    user8_cards = random.sample(pokes,4)
    for i in user8_cards:
        pokes.remove(i)
    user9_cards = random.sample(pokes,4)
    for i in user9_cards:
        pokes.remove(i)
    user10_cards = random.sample(pokes,4)
    for i in user10_cards:
        pokes.remove(i)
    return user1_cards,user2_cards,user3_cards,user4_cards,user5_cards,user6_cards,user7_cards,user8_cards,user9_cards,user10_cards

def get_ty_num(cards,ty_card):
    ty_card_num = cards.count(ty_card)
    for i in cards:
        if i in ['BJ','CJ']:
            ty_card_num += 1
    # print(ty_card_num)
    return ty_card_num

def cal_pro(cards,ty_card,ty_card_num):
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
                ['8','9','10','J'],['9','10','J','Q'],['10','J','Q','K']]
    print(cards_char)
    if ty_card_num == 0:
        #同花顺 例如：'2s','3s','4s','5s'
        if cards_char in shunzi4_list and ty_card not in [rand_cards[rand_cards.index(cards_char[0])-1],rand_cards[rand_cards.index(cards_char[-1])+1]] and cards[0][-1] == cards[1][-1] == cards[2][-1] == cards[3][-1]: 
            mag = 4
            bet = 4
        #有两对且相加和为10，例如：3，3，7，7
        elif len(list(set(cards_int))) == 2 and list(set(cards_int))[0] + list(set(cards_int))[1] == 10 and ty_card not in ['10','J','Q','K'] and cards_char.count(cards_char[0]) == 2:
            mag = 4
            bet = 4
        #四张牌是10,J,Q,K
        elif cards_char == ['10','J','Q','K'] and ty_card not in ['9','A']:
            mag = 4
            bet = 4
        #四张牌点数相同,例如：4，4，4，4
        elif len(list(set(cards_char))) == 1:
            mag = 4
            bet = 4
        else:
            mag = 0
            bet = 1
    elif ty_card_num == 1:
        print(cards_char)
        #癞子是K，有Q,例如：4，6，Q
        if ty_card == 'K' and cards_char[-1] == 'Q' :
            #前两张牌都小于10，且和也不等于10，例如：7，8，K
            if cards_int[0] < 10 and cards_int[1] < 10 and cards_int[0] + cards_int[1] != 10:
                mag = 0
                bet = 4
            else:
                mag = 4
                bet = 4
        #有K，例如:3,J,K
        elif cards_char[-1] == 'K':
            #前两张牌都小于10，且和也不等于10，例如：7，8，K
            if cards_int[0] < 10 and cards_int[1] < 10 and cards_int[0] + cards_int[1] != 10:
                mag = 0
                bet = 4
            else:
                mag = 4
                bet = 4
        #有一对，且有两张牌和为10，例如：4，6，4
        elif len(list(set(cards_int))) == 2 and list(set(cards_int))[0] + list(set(cards_int))[1] == 10 and ty_card not in ['10','J','Q','K']:
            mag = 4
            bet = 4
        #同花且是顺子中的三张,例如：4d，5d，6d
        elif cards[0][-1] == cards[1][-1] and cards[0][-1] == cards[2][-1] and int(rand_cards.index(cards_char[2])) - int(rand_cards.index(cards_char[0])) < 3 and len(list(set(cards_char))) == 3:
            mag = 4
            bet = 4
        #三张牌是10的倍数，且有一对，例如：7，7，6或者2，4，4
        elif len(list(set(cards_int))) == 2 and (cards_int[0] + cards_int[1] + cards_int[2] in [10,20]) and ty_card not in ['10','J','Q','K']:
            mag = 4
            bet = 4
        #三张点数相同，例如：5，5，5
        elif len(list(set(cards_char))) == 1:
            mag = 4
            bet = 4
        #三张花牌且不相等,例如：J,Q,K
        elif len(list(set(cards_char))) == 3 and all(x in ['10','J','Q','K'] for x in cards_char) and ty_card not in ['A','9','10','J','Q','K']:
            mag = 4
            bet = 4
        #两张牌或三张牌和是10的倍数，例如1,2,7或1，3，7或2，5，8或4，6，9或2，J，Q
        elif (cards_int[0] + cards_int[1] == 10 or cards_int[0] + cards_int[2] == 10 or cards_int[1] + cards_int[2] in [10,20] or cards_int[0] + cards_int[1] + cards_int[2] in [10,20]) and cards_char[-1] != 'K':
            mag = 3
            bet = 1
        elif len(list(set(cards_char))) == 3 and all(x in ['A','2','3'] for x in cards_char) and ty_card not in ['A','2','3','4','5']:
            mag = 0
            bet = 4
        else:
            mag = 0
            bet = 1
    elif ty_card_num == 2:
        if ty_card == 'K' and cards_char[1] == 'Q': #癞子是K，有Q
            mag = 4
            bet = 4 
        elif cards_char[1] == 'K':        #有K
            mag = 4 
            bet = 4
        elif int(rand_cards.index(cards_char[1])) - int(rand_cards.index(cards_char[0])) <= 3:                    #顺子或炸弹，例如：5，8
            mag = 4 
            bet = 4
        elif cards[0][-1] == cards[1][-1] and int(rand_cards.index(cards_char[1])) - int(rand_cards.index(cards_char[0])) <= 4: #同花顺，例如：5h,9h
            mag = 4
            bet = 4
        elif cards_int[0] + cards_int[1] == 10:          #比翼,炸弹，例如：3，7
            mag = 4 
            bet = 4
        elif cards[0][-1] == cards[1][-1]:   #同花,例如：4s,8s
            mag = 4 
            bet = 4
        else:           #'2s' ,'9c'
            mag = 3
            bet = 1
    elif ty_card_num == 3:
        mag = 4
        bet = 4
    elif ty_card_num == 4:
        mag = 4
        bet = 4
    return mag,bet

# for i in range(10):
# pokes,ty_card = get_poke(rand_cards,pokes)
# cards_list = send_cards(pokes)
# for i in cards_list:
# ty_card,my_cards = socket_client()
# ty_card_num = get_ty_num(my_cards,ty_card)
# m,b = cal_pro(my_cards,ty_card,ty_card_num)
# print('癞子数：%s'%ty_card_num,'抢庄：%s'%m,'下注：%s'%b)
#         # time.sleep(5)

#     pokes = ['3d', '3c', '3h', '3s', '4d', '4h', '4s', '4c', '5s', '5h', 
#     '5d', '5c', '6c', '6h', '6d', '6s', '7s', '7d', '7c', '7h', '8d', '8c',
#         '8s', '8h', '9s', '9d', '9h', '9c', '10s', '10d', '10h', '10c', 'Js', 
#         'Jc', 'Jd', 'Jh', 'Qh', 'Qc', 'Qs', 'Qd', 'Kd', 'Ks', 'Kc', 'Kh', 'As',
#         'Ah', 'Ac', 'Ad', '2d', '2h', '2s', '2c', 'BJ', 'CJ']















