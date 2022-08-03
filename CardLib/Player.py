import random

from CardLib import Hand, Card


class Player:
    def __init__(self, label: str, is_ai: bool = False):
        self.is_ai = is_ai
        self.hand = Hand([])
        self.label = label
        self.win_count = 0

    def __str__(self) -> str:
        return self.label + ': ' + str(self.hand)

    def get_label(self) -> str:
        return self.label

    def get_win_count(self) -> int:
        return self.win_count

    def round_winner(self):
        self.win_count = self.win_count + 1

    def get_amount_of_cards(self) -> int:
        return len(self.hand)

    def add_card_to_hand(self, card: Card):
        self.hand.add_card(card)

    def add_cards_to_hand(self, cards: [Card]):
        for card in cards:
            self.hand.add_card(card)

    def play_card(self, number: int = -1) -> Card:
        if self.is_ai:
            number = random.randint(0, len(self.hand) - 1)
        temp_card = self.hand.get_card_at(number)
        self.hand.rem_card(temp_card)
        return temp_card

    def clear_hand(self):
        self.hand.rem_all_cards()
