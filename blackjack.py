import simplegui
import random

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_hand = []
dealer_hand = []
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)

# load card sprite - 936x384 - source: jfitz.com
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        self.msg = "Hand contains:"
        for c in self.cards:
            self.msg = self.msg + " " + str(c)
        return self.msg

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        got_ace = False
        for c in self.cards:
            value = value + VALUES[c.get_rank()]
            if 'A' == c.get_rank():
                got_ace = True
                
        if (got_ace == False):
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else: 
                return value
   
    def draw(self, canvas, pos):
        hand_pos = pos
        for c in self.cards:
            c.draw(canvas, hand_pos)
            hand_pos[0] += CARD_SIZE[0] + 10

            
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
                

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        self.msg = "Deck contains:"
        for d in self.deck:
            self.msg = self.msg + " " + str(d)
        return self.msg            
            

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    
    if (in_play):
        outcome = "Game restarted, you lost. Hit or stand?"
        score -= 1
    else:
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())

        outcome = "New hand. Hit or stand?"
   
    in_play = True

def hit():
    global in_play, score, outcome
    if (in_play):
        if (player_hand.get_value() <= 21):
            player_hand.add_card(deck.deal_card())
            if (player_hand.get_value() > 21):
                in_play = False
                score = score - 1                
                outcome = "You have busted. New deal?"                
            else:
                outcome = "Hit or stand?"
    
       
def stand():
    global in_play, score, outcome
    if (in_play):
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            print "Dealer's hand: " + str(dealer_hand) + " value: " + str(dealer_hand.get_value())

        in_play = False
        
        if (dealer_hand.get_value() > 21):
            outcome = "Dealer has busted. You win!"
            score = score + 1
        elif (dealer_hand.get_value() >= player_hand.get_value()):
            outcome = "Dealer beat you!"
            score = score - 1
        else:
            outcome = "You won!"
            score = score + 1
       
    else:
        outcome = "Hand is over."
    
    outcome += " New deal?"    

# draw handler    
def draw(canvas):
    canvas.draw_text('B l a c k j a c k', (130, 60), 52, 'Orange')
    canvas.draw_text('Dealer', (100, 120), 22, 'White')
    dealer_hand.draw(canvas, [100, 150])
    if (in_play):
        canvas.draw_image(card_back, (CARD_CENTER[0], CARD_CENTER[1]), CARD_SIZE, [100 + CARD_CENTER[0], 150 + CARD_CENTER[1]], CARD_SIZE)
    canvas.draw_text('Player [ score: ' + str(score) + ' ]', (100, 370), 22, 'White')
    player_hand.draw(canvas, [100, 400])    
    canvas.draw_text(outcome, (100, 310), 30, 'Cyan')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
