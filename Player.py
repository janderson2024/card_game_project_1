class Player:
    def __init__(self, label):
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

    def play_card(self, number):
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