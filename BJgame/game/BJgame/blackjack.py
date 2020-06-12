import random

RANK, SUIT = 0, 1


def win_lose(dealer_hand, player_hand, bet, player_money, surrender=False):
    player_point = get_point(player_hand)
    dealer_point = get_point(dealer_hand)
    if surrender:
        return "<<You surrender.>>", player_money + int(bet/2)
    else:
        if player_point <= 21:
            if(player_point > dealer_point)or (dealer_point > 21):
                if player_point == 21:
                    return 'win', player_money+int(bet*2.5)
                else:
                    return 'win', player_money+bet*2

            elif player_point == dealer_point:
                if player_point == 21 and len(player_hand) > 3 and len(dealer_hand) == 2:
                    return 'lose', player_money
                else:
                    return '<<Push>>', player_money+bet

            else:
                return 'lose', player_money
        else:
            return 'bust', player_money


def player_op(deck, player_hand, op):
    surrender, doubled, ending = False, False, False
    if op == '1':
        print('[ Player : Stand ]')
        surrender, doubled, ending = False, False, True
    elif op == '2':
        print('[ Player : Hit ]')
        player_hand.append(deck.pop())
        print_player_hand(player_hand)
        surrender, doubled, ending = False, False, False

    elif op == '3':
        if len(player_hand) == 2:
            print('[ Player : Double down  ]')
            player_hand.append(deck.pop())
            print_player_hand(player_hand)
            surrender, doubled, ending = False, True, True

        else:
            print("( You can't double)")

    elif op == '4':
        if len(player_hand) == 2:
            print('[ Player : Surrender  ]')
            surrender, doubled, ending = True, False, True
        else:
            print("You can't surrender")

    if get_point(player_hand) > 21:
        print('You are busted!')
        ending = True
    return surrender, doubled, ending


def dealer_op(deck, player_hand, dealer_hand):
    while get_point(player_hand) <= 21:
        if get_point(dealer_hand) >= 17:
            print('[ Dealer : Stand ]')
            break
        else:
            print('[ Dealer : Hit ]')
            dealer_hand.append(deck.pop())
        print_dealer_hand(dealer_hand, False)


def get_point(hand):
    result = 0
    ace_flag = False
    for card in hand:
        if card[RANK] == 1:
            ace_flag = True
        if card[RANK] > 10:
            num = 10
        else:
            num = card[RANK]
        result += num
    if ace_flag and result <= 11:
        result += 10
    return result


def print_player_hand(player_hand):
    print('Player(', get_point(player_hand), '):   ')
    for card in player_hand:
        print('[', card[SUIT], card[RANK], ']')
    print()


def print_dealer_hand(dealer_hand, uncovered):
    if uncovered:
        print('Dealer(', get_point(dealer_hand), '):   ')
    else:
        print('dealer (??):   ')
    flag = True
    for card in dealer_hand:
        if flag or uncovered:
            print('[', card[SUIT], card[RANK], ']')
            flag = False
        else:
            print('[* *]')
    print()


def make_deck():
    suits = ['S', 'H', 'D', 'C']
    ranks = range(1, 14)
    deck = [(x, y)for x in ranks for y in suits]
    random.shuffle(deck)
    return deck


def main():
    turn = 1
    player_money = 100
    deck = make_deck()

    while(player_money > 0):
        print('-'*20)
        print('Turn:', turn)
        print('Your money:', player_money)
        print('-'*20)
        player_hand = []
        # split_hand
        dealer_hand = []
        Surrender = False

        try:
            bet = int(input('Bet >> '))
        except:
            print('Please enter an integer')
            continue

        if bet > player_money:
            print("You don't have enough money!")
            continue
        elif bet <= 0:
            print("Please enter a natural number")
            continue
        player_money -= bet
        if len(deck) < 10:
            deck = make_deck

        for i in range(2):
            player_hand.append(deck.pop())
            dealer_hand.append(deck.pop())

        print('-'*20)
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand, False)
        print('-'*20)

        while True:
            op = input('Stand:1,Hit:2,Double:3,Surrender:4 >')
            surrender, doubled, ending = player_op(deck, player_hand, op)
            if doubled:
                player_money -= bet
                bet += bet
            if surrender:
                Surrender = True
                break
            if ending:
                break

        dealer_op(deck, player_hand, dealer_hand)
        print('-'*20)
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand, True)
        print('-'*20)
        message, player_money = win_lose(
            dealer_hand, player_hand, bet, player_money, Surrender)
        print(message)

        turn += 1
        input('Go next')
    print('Game over!')


if __name__ == '__main__':
    main()
