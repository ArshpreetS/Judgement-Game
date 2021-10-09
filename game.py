import random


print("******** Welcome to play Judgement ********\n")
print("""
                      ____________
                     | A          |           J
                     |         ___|________   U
                     |    /\  | K          |  D 
                     |   /  \ |            |  G
                     |   \  / |     /\     |  E
                     |    \/  |    /  \    |  M
                     |        |    \  /    |  E
                     |________|     \/     |  N
                              |            |  T
                              |____________|
    
    """)
name = input("What is your name? ") # To enter your name!

judgement = {1:{}}
scores = {1:{"bot1":0,"bot2":0,"bot3":0,f"{name}":0}}
repeat = {"bot1":0,"bot2":0,"bot3":0,f"{name}":0}
values = {"A":14,"K":13,"Q":12,"J":11,"T":10,"10":10,"9":9,"8":8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2,"1":1}
l = ["D","H","C","S"]

cards_given = []

# Creating the cards for the game
cards = []
for j in l:
    for i in range(2,11):
        cards = cards + [j + str(i)]
    cards = cards + [j + "J"]
    cards = cards + [j + "Q"]
    cards = cards + [j + "K"]
    cards = cards + [j + "A"]
# Players of the game!
bot1 = []
bot2 = []
bot3 = []
use4 = []

#To show the cards
def show_cards(l):
    style = {"C":[],"S":[],"D":[],"H":[]}
    for x in l:
        style[x[0]].append(x)
    print(f""" Cards in Clubs: {style["C"]}\n Cards in Spades:{style["S"]}\n Cards in Diamonds: {style["D"]}\n Cards in Hearts: {style["H"]}\n""")
    
# Distribute the cards
def Give_Cards(player,cards_left,n): # n is the number of cards to be given
    s = random.sample(cards_left,n)
    player.extend(s)
    for i in s:
        cards_left.remove(i)

table = {}
roll_no = {}
players = {"bot1":bot1,"bot2":bot2,"bot3":bot3,f"{name}":use4}


# READ CARDS FROM THE FILE!
def read_cards():
    file_name = input("Enter the file name: ")

    #file_name = "readme.txt"
    with open(file_name,"r") as f:
        for i in range(4):
            s = f.readline()
            player, given_cards = [x.strip(" \n") for x in s.split(":")]
            players[player].extend([x for x in given_cards.split(",")])
            print()
        s = f.readline()
        order = s.split(",")
        global table
        for z in range(4):
            table[z] = order[z]
    for x in table:
        roll_no[table[x]] = x
    return (table,roll_no)

# Give cards to all the players
def shuffle_cards():
    cards_given = cards.copy()
    Give_Cards(bot1,cards_given,13)
    Give_Cards(bot2,cards_given,13)
    Give_Cards(bot3,cards_given,13)
    Give_Cards(use4,cards_given,13)
    print(f"\n\n***********************  {name}'s cards ********************")
    print(use4)


def normal():
    print(f"\nThe sequence of the game will be:\nBOT 1 --> BOT 2 --> BOT 3 --> {name}")

def play_game():
    if game >= 2:
        scores[game] = repeat.copy()
    global table, roll_no, players
    table = {}
    roll_no = {}
    if response.lower() == "b":
        table = {0:"bot1",1:"bot2",2:"bot3",3:f"{name}"}
        for b in range(4):
            roll_no[table[b]] = b
    else:
        table,roll_no = read_cards()
        players = {"bot1":bot1,"bot2":bot2,"bot3":bot3,f"{name}":use4}


    # Take judgements!!
    judge_bot1 = judge(bot1)
    judge_bot2 = judge(bot2)
    judge_bot3 = judge(bot3)
    
    
    # Make a Judgement
    print("******* Take Judgement **********")
    print(f"BOT 1 --->  {judge(bot1)}")
    print(f"BOT 2 --->  {judge(bot2)}")
    print(f"BOT 3 --->  {judge(bot3)}")
    user_judge = int(input("Your judgement: "))
    judge_user = user_judge
    print(f"{name} ---> {judge_user}")
    judgement[game] = {}
    judgement[game]["bot1"] = judge_bot1
    judgement[game]["bot2"] = judge_bot2
    judgement[game]["bot3"] = judge_bot3
    judgement[game][f"{name}"] = user_judge
    
    if response == "b":
        turn = random.sample([0,1,2,3],1)[0] 
    else:
        turn = 0
    # TAKING REST OF TURN
    for x in range(13):
        Chaal = []
        print(f"***************** ROUND {x+1} ****************")

        if x == 0:
            print(f"The game is starting with {table[turn]}\n")

        if table[turn] == f"{name}":
                print("_____________YOUR TURN_____________")
                print("((((((((((( YOUR CARDS ))))))))))))")
                show_cards(use4)
                use4_card = input("Enter your card: ")
                while use4_card not in use4:
                    print("card not in your deck!")
                    use4_card = input("Enter your card: ")
                suit_curr = use4_card[0]
                mx = values[use4_card[1:]]
                Chaal.append((f"{name}",values[use4_card[1:]]))
                use4.remove(use4_card)
        else:
            # First chaal
            mx = 0
            card1 = ""
            for i in players[table[turn]]:
                if values[i[1:]] > mx:
                    card1 = i
                    mx = values[i[1:]]
            first_card = card1
            suit_curr = card1[0]
            print(f"{table[turn]} --> {first_card}")
            Chaal.append((table[turn],values[first_card[1:]]))
            players[table[turn]].remove(first_card)

        for j in range(1,4):
            if table[(turn+j)%4] == f"{name}":
                print("_____________YOUR TURN_____________\n\n")
                print("(((((((((( YOUR CARDS )))))))))))")
                show_cards(use4)
                use4_card = input("Enter your card: ")
                while use4_card not in use4:
                    print("Card not in deck!")
                    use4_card = input("Enter your card: ")
                print(f"{name} --> {use4_card}")
                if use4_card[0] == suit_curr:
                    Chaal.append((f"{name}",values[use4_card[1:]]))
                    if values[use4_card[1:]] > mx:
                        mx = values[use4_card[1:]]
                use4.remove(use4_card)
            else:
                second_card,mx = take_turn(available = players[table[(turn+j)%4]],suit = suit_curr,high = mx)
                print(f"{table[(turn+j)%4]} --> {second_card}")
                if second_card[0] == suit_curr:
                    Chaal.append((table[(turn+j)%4],values[second_card[1:]]))
                players[table[(turn+j)%4]].remove(second_card)
        turn = int(normal_comparison(Chaal))
        scores[game][table[(turn)]] += 1
        print(scores[game])
        print(f"___________ The round is won by {table[turn]} ___________\n")

    # The game is over, now is the time for scores
    print("********************* SCORES ***********************")
    bored = []
    for i in range(4):
        x = judgement[game][table[i]]
        y = scores[game][table[i]]
        if (x>y):
            print(f"{table[i]} -> {-10*x}")
            bored.append((table[i],-10*x))
        else:
            print(f"{table[i]} -> {10*x + (y-x)}")
            bored.append((table[i],10*x + (y-x)))
    bored.sort(key = lambda x:x[1])
    print(f"{bored[3][0]} is the winner!!!")
def take_turn(available,suit,high):
    mx = 0
    mn = 14
    card_max = ""
    card_min = ""
    for x in available:
        if x[0] == suit and values[x[1:]] > mx:
            card_max = x
            mx = values[x[1:]]
        if x[0] == suit and values[x[1:]] < mn:
            card_min = x
            mn = values[x[1:]]
    if mx > high:
        return card_max,mx
    else:
        if (mn != 14):
            return card_min,high
        else:
            final_card = ""
            for y in available:
                if values[y[1:]] < mn:
                     final_card = y
                     mn = values[y[1:]]
            return final_card,high

# TO GIVE A JUDGEMENT
def judge(player):
    count = 0
    for i in player:
        if (i[1:].isalpha()):
            count += 1
    return count


# THIS IS TO COMPARE THE CARDS THROWN IN THE ROUND
def normal_comparison(l):
    l.sort(key = lambda x: x[1])
    player,card = l[-1]
    return roll_no[player]


play = "y"
game = 1
while play[0].lower() == "y":
    response = ""
    while response.lower() not in ["a","b"]:
        print("How do you want to play the game?\nA --> with an input file\nB --> Normally")
        response = input()
    if response.lower() == "a":
        play_game()
    elif response.lower() == "b":
        normal()
        shuffle_cards()
        play_game()
    game = game + 1
    play = input("Do you want to play another game: ")

if play[0].lower() != "y":
    print("************* FINAL SCORES *************")
    f_scores = {}
    bored2 = []
    for z in scores:
        for i in scores[z]:
            x = judgement[z][i]
            y = scores[z][i]
            if (x>y):
                f_scores[i] = f_scores.get(i,0) - 10*x 
            else:
                f_scores[i] = f_scores.get(i,0) + 10*x + (y-x)
    print(f_scores)
    for s in f_scores:
        bored2.append((s,f_scores[s]))
    bored2.sort(key = lambda x:x[1])
    print(f"Overall winner is {bored2[3][0]}!!!")