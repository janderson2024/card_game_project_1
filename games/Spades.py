import random

import CardLib
from decimal import *

from CardLib.cardlists import CardList
from CardLib.cardlists import Hand
from CardLib import Card, Player


def start_game():
    game = Spades()
    game.setup_game()
    game.main_loop()


def get_bid(player: Player) -> int:
    hand = player.hand
    if player.is_ai:
        strengths = [get_strength(card) for card in hand.card_list]
        strength = int(sum(strengths) // 1)
        if hand.num_cards_left() > 9:
            strength += 1
        if strength < 1:
            strength = 1
        return strength
    else:
        return int(CardLib.get_user_input([str(num + 1) for num in range(hand.num_cards_left())],
                                          str(hand) + "\nHow many tricks would you like to bid?")[0])


def get_strength(card: Card) -> float:
    if card.value >= 14:
        return 1
    elif card.value >= 12:
        return .4
    elif card.suit_text == CardLib.SPADE:
        return .25
    else:
        return 0


def split_trump(cards: CardList):
    lead_suit = cards.card_list[0].suit
    spades = [card for card in cards.card_list if card.suit == CardLib.SPADE or card.suit == CardLib.JOKER]
    lead = [card for card in cards.card_list if card.suit == lead_suit]
    return spades, lead


def calc_score(bid: int, trick: int) -> int:
    if bid <= trick:
        return bid * 10 + (trick - bid)
    else:
        return 0


def loss_count(card: Card, cards: Hand, card_to_beat: Card) -> Decimal:
    cards.add_card(card)
    if card_to_beat:
        cards.add_card(card_to_beat)
        cards.sort_by_suit()
        card_index = Decimal(cards.card_list.index(card))
        card_to_beat_index = Decimal(cards.card_list.index(card_to_beat))
        cards.rem_cards([card, card_to_beat])
        if card_to_beat_index < card_index:
            return Decimal(cards.num_cards_left())
        else:
            return card_index
    else:
        same_suit = CardLib.Hand([c for c in cards if c.suit == card.suit])
        same_suit.sort_by_rank()
        cards.rem_card(card)
        return Decimal(same_suit.card_list.index(card))


def get_ratio(card: Card, cards: CardList, card_to_beat: Card) -> Decimal:
    losses = loss_count(card, cards, card_to_beat)
    total = Decimal(cards.num_cards_left())
    return (total - losses) / total


class Spades:
    WINNING_SCORE = 150

    def __init__(self):
        self.scores = None
        self.player_count = None
        self.player_list = None
        self.pot = None
        self.tricks = None
        self.leader = None
        self.bids = None
        self.spades_broken = None
        self.discard = CardLib.Discard()

    def setup_game(self):
        count, none = CardLib.get_user_input(["4", "6"], "How many players?")
        self.player_count = int(count)
        self.player_list = [CardLib.Player("Player")]
        self.scores = [0]

        for num in range(1, int(self.player_count)):
            self.player_list.append(CardLib.Player("AI #" + str(num), is_ai=True))
            self.scores.append(0)

    def main_loop(self):
        while self.is_no_winner():
            self.spades_broken = False
            self.setup_hand()
            self.get_bids()
            print("\n\n\n-----Bids----: " + str(self.bids))
            self.leader = self.bids.index(max(self.bids))
            self.do_hand()
            print("-----Bids----: " + str(self.bids))
            print("----Tricks---: " + str(self.tricks))
            new_scores = self.get_scores()
            self.scores = [old + new for old, new in zip(self.scores, new_scores)]
            print("----Scores---: " + str(self.scores))

    def is_no_winner(self) -> bool:
        return [score for score in self.scores if score >= self.WINNING_SCORE] == []

    def setup_hand(self):
        pack = self.get_pack()
        pack.shuffle()
        pack, self.player_list = CardLib.deal_to_players(pack, self.player_list,
                                                         pack.num_cards_left() // self.player_count)
        [player.hand.sort_by_suit() for player in self.player_list]

    def get_pack(self) -> CardList:
        pack = CardLib.Draw([])
        if self.player_count == 4:
            CardLib.fill_deck_standard_52(pack, ace_high=True)
        elif self.player_count == 6:
            CardLib.fill_deck_standard_54(pack, ace_high=True)
            pack.get_card_at(-1).suit = CardLib.SPADE
            pack.get_card_at(-2).suit = CardLib.SPADE
        return pack

    def get_bids(self) -> [int]:
        self.bids = [get_bid(player) for player in self.player_list]

    def do_hand(self):
        self.tricks = [0 for _ in range(self.player_count)]
        self.discard = CardLib.CardList()
        while self.player_list[0].hand.num_cards_left() > 0:
            print("---Discard---: " + str(self.discard))
            print("----Tricks---: " + str(self.tricks))
            self.do_round()
            self.tricks[self.leader] += 1

    def do_round(self):
        self.pot = CardLib.CardList()
        while self.pot.num_cards_left() < self.player_count:
            self.player_list[self.leader] = self.get_play(self.player_list[self.leader])
            print("---Player " + str(self.leader + 1) + "--: Played " + str(self.pot.get_card_at(-1)))
            self.leader = self.next_player(self.leader)
        winning_card = self.get_winning_card()
        self.leader = self.pot.get_card_list().index(winning_card) + self.leader
        if self.leader >= self.player_count:
            self.leader -= self.player_count
        print("---Player " + str(self.leader + 1) + "--: Takes the trick ")
        self.discard.add_cards(self.pot)

    def get_play(self, player: Player):
        valid_plays = self.get_valid_plays(self.pot, player.hand)
        if player.is_ai:
            play = self.get_ai_play(valid_plays, player.hand)
        else:
            play = valid_plays.get_card_at(
                int(CardLib.get_user_input([str(num + 1) for num in range(valid_plays.num_cards_left())],
                                           "-----Pot-----: " + str(self.pot) + "\n" +
                                           "-----Hand----: " + str(player.hand) + "\n" +
                                           "-Valid Plays-: " + str(valid_plays))[0]) - 1)
        self.pot.add_card(play)
        player.hand.rem_card(play)
        if not self.spades_broken:
            if play.suit == CardLib.SPADE:
                self.spades_broken = True
                print("Spades Broken:")
        return player

    def get_valid_plays(self, pot: CardList, hand: Hand) -> Hand:
        cards = CardLib.Hand([])
        if pot.num_cards_left() == 0:
            if self.spades_broken:
                cards.add_cards(hand.get_card_list())
            else:
                cards.add_cards([card for card in hand.card_list if card.suit != CardLib.SPADE])
        else:
            led_card = pot.get_card_at(0)
            cards.add_cards([card for card in hand.card_list if card.suit == led_card.suit])
            if cards.num_cards_left() == 0:
                cards.add_cards(hand.get_card_list())
        return cards

    def get_ai_play(self, valid_plays: CardList, hand: Hand) -> Card:
        if valid_plays.num_cards_left() == 1:
            return valid_plays.get_card_at(0)
        if self.pot:
            card_to_beat = self.get_winning_card()
        else:
            card_to_beat = None
        ratios = self.winning_ratios(card_to_beat, valid_plays, hand)
        return random.choices(valid_plays.card_list, weights=ratios)[0]

    def winning_ratios(self, card_to_beat: Card, plays: CardList, hand: Hand) -> [Decimal]:
        pack = self.get_pack()
        pack.rem_cards(self.discard)
        pack.rem_cards(hand)
        if self.pot:
            pack.rem_cards(self.pot)
            lead_suit = self.pot.card_list[0].suit
            possible_losses = CardLib.Hand(
                [card for card in pack.card_list if card.suit == CardLib.SPADE or card.suit == lead_suit])
        else:
            possible_losses = CardLib.Hand(pack.card_list)
        ratios = [get_ratio(card, possible_losses, card_to_beat) for card in plays]
        remaining_plays = (self.player_count - self.pot.num_cards_left()) - 1
        output = []
        for ratio in ratios:
            try:
                output.append(float(ratio ** remaining_plays))
            except InvalidOperation:
                output.append(0)
        return output

    def next_player(self, leader: int) -> int:
        if leader >= self.player_count - 1:
            return 0
        else:
            return leader + 1

    def get_winning_card(self) -> Card:
        spades, lead = split_trump(self.pot)
        if len(spades) == 0:
            return CardLib.get_highest_card(CardLib.CardList(lead))
        else:
            return CardLib.get_highest_card(CardLib.CardList(spades))

    def get_scores(self) -> [int]:
        return [calc_score(bid, trick) for (bid, trick) in zip(self.bids, self.tricks)]
