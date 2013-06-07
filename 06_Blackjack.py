# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
wins = 0
loses = 0
game_no = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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
        result = ""
        for card in self.cards:
            result += str(card) + ' '
        return result
        
    def add_card(self, card):
        self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        value = 0
        a_count = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                a_count += 1
        if value + 10 <= 21 and a_count >= 1:
            value += 10
        return value
        
    def is_busted(self):
        return self.get_value() > 21
    
    def clear(self):
        self.cards = []
    
    def draw(self, canvas, p, in_play):
        if not in_play:
            for i in range(len(self.cards)):
                self.cards[i].draw(canvas, [p[0] + (i % 5) * 90, p[1] + (i // 5) * 110])
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                              [p[0] + CARD_BACK_CENTER[0], p[1] + CARD_BACK_CENTER[1]],
                              CARD_BACK_SIZE)
            for i in range(1, len(self.cards)):
                self.cards[i].draw(canvas, [p[0] + (i % 5) * 90, p[1] + (i // 5) * 110])
        
            
        
# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(s ,r) for s in SUITS for r in RANKS]
        self.i = -1
    # add cards back to deck and shuffle
    def shuffle(self):
        self.i = -1
        random.shuffle(self.cards)

    def deal_card(self):
        self.i += 1
        return self.cards[self.i]


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, game_no, loses
    player_hand = Hand()
    dealer_hand = Hand()
    deck.shuffle()
    game_no += 1
    if in_play:
        loses += 1
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    outcome = "Hit or stand?"
    in_play = True
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
def hit():
    global loses, outcome, in_play
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.is_busted():
            outcome = 'You have busted. Please press new deal for restaring game?'
            loses += 1
            in_play = False
            
def stand():
    global wins, loses, outcome, in_play
    if in_play:
        in_play = False
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.is_busted():
            wins += 1
            outcome = 'You won. Please press new deal for restaring game?'
        elif dealer_hand.get_value() >= player_hand.get_value():
            loses += 1
            outcome = 'You lose. Please press new deal for restaring game?'
        else:
            wins += 1
            outcome = 'You won. Please press new deal for restaring game?'
            

    
# draw handler    
def draw(canvas):

    canvas.draw_text("Player " + str(wins) + ':' + str(loses) + " Dealer", [325, 25], 24, "Black")
    canvas.draw_text("Number of games:" + str(game_no), [325, 45], 18, "yellow")
    canvas.draw_text(outcome, [100, 625], 20, "white")
    canvas.draw_text("Vegas dealer", [10, 25], 24, "Yellow")
    canvas.draw_text("You", [10, 425], 24, "Yellow")
    
    dealer_hand.draw(canvas, [200, 200], in_play)
    player_hand.draw(canvas, [200, 650], False)

    


# initialization frame
frame = simplegui.create_frame("Blackjack", 1000, 1000)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# deal an initial hand
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric