import random

class Player:
    def __init__(self, label, is_ai=False):
        self.is_ai = is_ai
        self.deck = []
        self.label = label
        self.win_count = 0

    def __str__(self):
        return self.label + ': ' + ' '.join([f"{str(num)}) {str(card)}" for num, card in enumerate(self.deck, start=1)])
        
    def get_label(self):
        return self.label

    def get_win_count(self):
        return self.win_count

    def round_winner(self):
        self.win_count = self.win_count + 1

    def add_cards(self, cards):
        for card in cards:
            self.deck.append(card)

    def get_card_num(self):
        return len(self.deck)

    def play_card(self, number =-1):
        if self.is_ai:
            number = random.randint(0, len(self.deck) - 1)
        tempcard = self.deck[number]
        del self.deck[number]
        return tempcard

    def reset_deck(self):
        self.deck = []

    #test code :
    # user = Player("Player 1")
    # user.add_cards([Card(1,1), Card(1,2), Card(1,3)])
    # print(user)
    # print(user.play_card(1))
    # print(user)

    # ai1 = Player("AI1", True)
    # ai1.add_cards([Card(1,1), Card(1,2), Card(1,3), Card(1,4), Card(1,5), Card(1,6)])
    # print(ai1)
    # ai1.play_card()
    # print(ai1)