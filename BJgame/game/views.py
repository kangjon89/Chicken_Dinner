from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponse
import random
import game.BJgame.blackjack as bj
import game.BJgame.redis_helper as r
from login.models import User
# Create your views here.

Index = [0,1,2,3,4,5,6,7,8,9,10]

def conv_image_path(list):
    tmp = []
    for i in list:
        s = str(i[1])+"_"+str(i[0]).zfill(2)+".png"
        tmp.append(s)
    return tmp


def game(request):
    if request.method == 'GET':
        token = str(random.random())
        request.session['token'] = token

        request.session['round_count'] = 1

        r.set_redis(token, 'game_now', False)
        

        deck = bj.make_deck()

        r.set_redis(token, 'deck', deck)
        if int(request.session['user_money']) < 10:
            r.set_redis(token, 'money', 100)
        else:
            r.set_redis(token, 'money', request.session['user_money'])
        r.set_redis(token, 'bet', 0)

        r.set_redis(token, 'player_hands', [])
        r.set_redis(token, 'dealer_hands', [])
        if int(request.session['user_money']) < 10:
            request.session['user_money'] = 100

        context = {

            'msg': 'Please bet',
            'dealer_cards': [],
            'dealer_point': 0,
            'player_cards': [],
            'player_point': 0,
            'able_bet': True,
            'isResult':False,
            'money': request.session['user_money'],
        }
        context.update(csrf(request))
        return render(request, "game.html", context)
    elif request.method == 'POST':
        token = request.session['token']
        deck = r.get_redis(token, 'deck')
        money = r.get_redis(token, 'money')

        player_hands = r.get_redis(token, 'player_hands')
        dealer_hands = r.get_redis(token, 'dealer_hands')

        if(r.get_redis(token, 'game_now') == False):
            try:
                if money < int(request.POST['bet']):
                    raise ValueError("You don't have enough money")
            except ValueError:
                msg = "Bet correctly"
                context = {

                    'msg': msg,
                    'dealer_cards': [],
                    'dealer_point': 0,
                    'player_cards': [],
                    'player_point': 0,
                    'able_bet': True,
                    'isResult':False,
                    'money': money,
                }
                context.update(csrf(request))
                return render(request, "game.html", context)
            r.set_redis(token, 'game_now', True)
            money -= int(request.POST['bet'])
            r.set_redis(token, 'money', money)
            r.set_redis(token, 'bet', int(request.POST['bet']))
            dealer_hands = []
            dealer_hands.append(deck.pop())
            player_hands = []
            player_hands.append(deck.pop())
            player_hands.append(deck.pop())
            r.set_redis(token, 'dealer_hands', dealer_hands)
            r.set_redis(token, 'player_hands', player_hands)
            dealer_point = bj.get_point(dealer_hands)
            player_point = bj.get_point(player_hands)
            r.set_redis(token, 'deck', deck)
            context = {
                'index':Index,
                'able_double': True,
                'msg': 'Please select',
                'dealer_cards': conv_image_path(dealer_hands),
                'dealer_point': dealer_point,
                'player_cards': conv_image_path(player_hands),
                'player_point': player_point,
                'able_bet': False,
                'isResult':False,
                'money': money,
                'bet': int(request.POST['bet']),
            }
            context.update(csrf(request))
            return render(request, "game.html", context)
        else:
            op = request.POST['operation']
            bet = r.get_redis(token, 'bet')
            surrender, doubled, ending = bj.player_op(deck, player_hands, op)
            r.set_redis(token, 'player_hands', player_hands)
            r.set_redis(token, 'deck', deck)
            player_point = bj.get_point(player_hands)

            print(player_hands)
            if doubled:
                bet = r.get_redis(token, 'bet')
                money -= bet
                bet *= 2
                r.set_redis(token, 'money', money)
                r.set_redis(token, 'bet', bet)
            if ending:
                dealer_hands.append(deck.pop())
                bj.dealer_op(deck, player_hands, dealer_hands)
                r.set_redis(token, 'dealer_hands', dealer_hands)

                dealer_point = bj.get_point(dealer_hands)
                player_point = bj.get_point(player_hands)

                msg, money = bj.win_lose(
                    dealer_hands, player_hands, bet, money, surrender)

                
                a = User.objects.get(id=request.session['user_id'])
                a.money = money
                a.save()
                request.session['user_money'] = money

                r.set_redis(token, 'money', money)
                # msg += 'Please bet'

                context = {
                    'index':Index,
                    'msg': msg,
                    'dealer_cards': conv_image_path(dealer_hands),
                    'dealer_point': bj.get_point(dealer_hands),
                    'player_cards': conv_image_path(player_hands),
                    'player_point': bj.get_point(player_hands),
                    'able_bet': True,
                    'isResult':True,
                    'money': money,
                }

                context.update(csrf(request))
                deck = bj.make_deck()
                r.set_redis(token, 'deck', deck)
                r.set_redis(token, 'game_now', False)
                request.session['result']=msg
                if money <= 0:
                    request.session['gameover']=True
                else:
                    request.session['gameover']=False

                return render(request, "game.html", context)
            else:
                r.set_redis(token, 'deck', deck)
                context = {
                    'index':Index,
                    'able_double': False,
                    'dealer_cards': conv_image_path(dealer_hands),
                    'dealer_point': bj.get_point(dealer_hands),
                    'player_cards': conv_image_path(player_hands),
                    'player_point': player_point,
                    'able_bet': False,
                    'isResult':False,
                    'money': money,
                    'bet': bet,
                }
                context.update(csrf(request))
                return render(request, "game.html", context)
                
def result(request):
    if request.session['result']=="win":
        print(request.session['result'])
        return render(request,'win.html')
    elif request.session['result'] == "lose": 
        print(request.session['result'])
        return render(request,"lose.html")
    elif request.session['result'] == "bust": 
        print(request.session['result'])
        return render(request,"lose.html")
    else:
        print(request.session['result'])
        return render(request,"draw.html")
def gameover(request):
    return render(request,"gameover.html")
