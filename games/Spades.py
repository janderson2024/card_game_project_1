import random
import time

import CardLib
from decimal import *

from CardLib.cardlists import CardList
from CardLib.cardlists import Hand
from CardLib import Card, Player


def start_game():
    CardLib.gui.start_gui("Spades!", 1000, 800)
    game = Spades()
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
        return get_player_bid(hand.num_cards_left())


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


def main_menu() -> str:
    CardLib.gui.remove_all_obj()
    title = CardLib.gui.GuiLabel(" SPADES ", x=450, y=100)
    prompt = CardLib.gui.GuiLabel("Main Menu", x=450, y=260)
    play = CardLib.gui.GuiButton(" Play ", x=475, y=400)
    info = CardLib.gui.GuiButton(" Help ", x=475, y=500)
    end = CardLib.gui.GuiButton(" Quit ", x=475, y=600)

    CardLib.gui.add_obj_to_be_drawn(title)
    CardLib.gui.add_obj_to_be_drawn(prompt)
    CardLib.gui.add_obj_to_be_drawn(play)
    CardLib.gui.add_obj_to_be_drawn(info)
    CardLib.gui.add_obj_to_be_drawn(end)

    choice = CardLib.gui.get_gui_user_input([play, info, end])
    CardLib.gui.remove_all_obj()

    if choice == play:
        return "play"
    elif choice == info:
        return "help"
    else:
        return "quit"


def how_to_play():
    title = CardLib.gui.GuiLabel(" How To Play ", x=400, y=50)
    rules = [CardLib.gui.GuiLabel("The entire deck is dealt out so each player should have the ", x=50, y=100),
             CardLib.gui.GuiLabel("same amount of cards.", x=50, y=150),
             CardLib.gui.GuiLabel("Each player decides how many tricks they will be able to take.", x=50, y=200),
             CardLib.gui.GuiLabel("There is only one round of bidding, and the minimum bid is 1.", x=50, y=250),
             CardLib.gui.GuiLabel("The first highest bid starts by playing a card.", x=50, y=300),
             CardLib.gui.GuiLabel("Spades cannot be led until one is played.", x=50, y=350),
             CardLib.gui.GuiLabel("Players must follow suit, if possible. If a player cannot ", x=50, y=400),
             CardLib.gui.GuiLabel("follow suit, they may play any card, including a spade.", x=50, y=450),
             CardLib.gui.GuiLabel("Spades are always higher than other suits.", x=50, y=500),
             CardLib.gui.GuiLabel("Whoever played the highest card takes the trick and leads next.", x=50, y=550),
             CardLib.gui.GuiLabel("Once all cards are played scores are calculated", x=50, y=600),
             CardLib.gui.GuiLabel("If the player made their bid they get their bid x 10 plus ", x=50, y=650),
             CardLib.gui.GuiLabel("1 for each extra trick. First to 150 wins!", x=50, y=700)]
    okay = CardLib.gui.GuiButton(" Okay ", x=450, y=750)

    CardLib.gui.add_obj_to_be_drawn(title)
    for rule in rules:
        CardLib.gui.add_obj_to_be_drawn(rule)
    CardLib.gui.add_obj_to_be_drawn(okay)

    choice = CardLib.gui.get_gui_user_input([okay])
    CardLib.gui.remove_all_obj()


def show_winner(winner, scores):
    CardLib.gui.remove_all_obj()
    title = CardLib.gui.GuiLabel(str(winner) + " wins!", x=400, y=150)
    score_label = CardLib.gui.GuiLabel("Scores", x=450, y=300)
    score_card = CardLib.gui.GuiLabel(", ".join([str(score) for score in scores]), x=400, y=350)
    okay = CardLib.gui.GuiButton(" Okay ", x=450, y=550)

    CardLib.gui.add_obj_to_be_drawn(title)
    CardLib.gui.add_obj_to_be_drawn(score_label)
    CardLib.gui.add_obj_to_be_drawn(score_card)
    CardLib.gui.add_obj_to_be_drawn(okay)

    choice = CardLib.gui.get_gui_user_input([okay])
    CardLib.gui.remove_all_obj()


def get_player_count():
    prompt = CardLib.gui.GuiLabel("How many players?", x=400, y=260)
    four = CardLib.gui.GuiButton(" 4 ", x=410, y=400)
    six = CardLib.gui.GuiButton(" 6 ", x=600, y=400)

    CardLib.gui.add_obj_to_be_drawn(prompt)
    CardLib.gui.add_obj_to_be_drawn(four)
    CardLib.gui.add_obj_to_be_drawn(six)

    choice = CardLib.gui.get_gui_user_input([four, six])
    CardLib.gui.remove_all_obj()

    if choice == four:
        return 4
    else:
        return 6


def get_player_bid(hand_size):
    prompt = CardLib.gui.GuiLabel("How much you like to bid?", x=350, y=350)
    numbers = [CardLib.gui.GuiButton(" 1 ", x=450, y=400),
               CardLib.gui.GuiButton(" 2 ", x=500, y=400),
               CardLib.gui.GuiButton(" 3 ", x=550, y=400),
               CardLib.gui.GuiButton(" 4 ", x=450, y=450),
               CardLib.gui.GuiButton(" 5 ", x=500, y=450),
               CardLib.gui.GuiButton(" 6 ", x=550, y=450),
               CardLib.gui.GuiButton(" 7 ", x=450, y=500),
               CardLib.gui.GuiButton(" 8 ", x=500, y=500),
               CardLib.gui.GuiButton(" 9 ", x=550, y=500),
               CardLib.gui.GuiButton(" 10 ", x=450, y=550),
               CardLib.gui.GuiButton(" 11 ", x=500, y=550),
               CardLib.gui.GuiButton(" 12 ", x=550, y=550),
               CardLib.gui.GuiButton(" 13 ", x=500, y=600)]

    CardLib.gui.add_obj_to_be_drawn(prompt)
    i = 0
    while i < hand_size:
        CardLib.gui.add_obj_to_be_drawn(numbers[i])
        i += 1

    choice = CardLib.gui.get_gui_user_input(numbers)
    CardLib.gui.remove_all_obj()

    return numbers.index(choice) + 1


class Spades:
    winning_score = 150

    def __init__(self):
        self.curr_hand = None
        self.scores = [0, 0, 0, 0, 0, 0]
        self.player_count = None
        self.player_list = None
        self.pot = None
        self.tricks = [0, 0, 0, 0, 0, 0]
        self.leader = None
        self.bids = [0, 0, 0, 0, 0, 0]
        self.spades_broken = None
        self.discard = CardLib.Discard([], x=-100, y=-100)

    def setup_game(self):
        count = get_player_count()
        self.player_count = int(count)
        if count == 4:
            player_locations = [(5, 650), (10, 325), (450, 10), (800, 325)]
        else:
            player_locations = [(155, 650), (10, 325), (10, 10), (450, 10), (800, 10), (800, 325)]
        self.player_list = [CardLib.Player("Player", x=player_locations[0][0], y=player_locations[0][1])]
        self.scores = [0]

        for num in range(1, int(self.player_count)):
            self.player_list.append(CardLib.Player("AI #" + str(num), is_ai=True,
                                                   x=player_locations[num][0], y=player_locations[num][1]))
            self.scores.append(0)

    def main_loop(self):
        playing = True
        while playing:
            choice = main_menu()
            if choice == "play":
                self.setup_game()
                self.game_loop()
            elif choice == "help":
                how_to_play()
            else:
                playing = False

    def game_loop(self):
        while self.is_no_winner():
            self.add_player_ui()
            self.spades_broken = False
            self.setup_hand()
            CardLib.gui.redraw()
            self.get_bids()
            self.add_player_ui()
            CardLib.gui.redraw()
            self.leader = self.bids.index(max(self.bids))
            self.do_hand()
            new_scores = self.get_scores()
            self.scores = [old + new for old, new in zip(self.scores, new_scores)]
            CardLib.gui.redraw()
        player_number = self.scores.index(max(self.scores))
        show_winner(self.player_list[player_number], self.scores)

    def add_player_ui(self):
        CardLib.gui.remove_all_obj()
        if self.player_count == 4:
            player_locations = [(5, 650), (10, 325), (450, 10), (800, 325)]
        else:
            player_locations = [(155, 650), (10, 325), (10, 10), (450, 10), (800, 10), (800, 325)]
        bid_locations = [(x + 100, y + 115) for (x, y) in player_locations]
        trick_locations = [(x + 55, y + 150) for (x, y) in player_locations]
        score_locations = [(x + 55, y + 185) for (x, y) in player_locations]
        for player in self.player_list:
            i = self.player_list.index(player)
            if i == 0:
                bid_label = CardLib.gui.GuiLabel(
                    "Bid " + str(self.bids[i]), bid_locations[i][0], player_locations[i][1])
                trick_label = CardLib.gui.GuiLabel(
                    "Tricks " + str(self.tricks[i]), trick_locations[i][0] + 150, player_locations[i][1])
                score_label = CardLib.gui.GuiLabel(
                    "Score " + str(self.scores[i]), score_locations[i][0] + 300, player_locations[i][1])
            else:
                bid_label = CardLib.gui.GuiLabel(
                    "Bid " + str(self.bids[i]), bid_locations[i][0], bid_locations[i][1])
                trick_label = CardLib.gui.GuiLabel(
                    "Tricks " + str(self.tricks[i]), trick_locations[i][0], trick_locations[i][1])
                score_label = CardLib.gui.GuiLabel(
                    "Score " + str(self.scores[i]), score_locations[i][0], score_locations[i][1])
            CardLib.gui.add_obj_to_be_drawn(bid_label)
            CardLib.gui.add_obj_to_be_drawn(score_label)
            CardLib.gui.add_obj_to_be_drawn(trick_label)
            CardLib.gui.add_obj_to_be_drawn(player)
            player.hand.sort_by_suit()
            player.hand.update_cards_pos()
            CardLib.gui.redraw()

    def is_no_winner(self) -> bool:
        return [score for score in self.scores if score >= self.winning_score] == []

    def setup_hand(self):
        pack = self.get_pack()
        pack.shuffle()
        pack, self.player_list = CardLib.deal_to_players(pack, self.player_list,
                                                         pack.num_cards_left() // self.player_count)
        [player.hand.sort_by_suit() for player in self.player_list]
        self.player_list[0].hand.update_cards_pos()

    def get_pack(self) -> CardList:
        pack = CardLib.DrawPile([])
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
        self.add_player_ui()
        self.discard = CardLib.CardList([], -100, -100)
        while self.player_list[0].hand.num_cards_left() > 0:
            CardLib.gui.redraw()
            self.do_round()
            self.tricks[self.leader] += 1
            self.add_player_ui()
            CardLib.gui.redraw()

    def do_round(self):
        self.pot = CardLib.CardList([], 250, 350)
        CardLib.gui.add_obj_to_be_drawn(self.pot)
        time.sleep(0.5)
        while self.pot.num_cards_left() < self.player_count:
            self.player_list[self.leader] = self.get_play(self.player_list[self.leader])
            time.sleep(0.5)
            self.leader = self.next_player(self.leader)
        winning_card = self.get_winning_card()
        self.leader = self.pot.get_card_list().index(winning_card) + self.leader
        if self.leader >= self.player_count:
            self.leader -= self.player_count
        self.discard.add_cards(self.pot)

    def get_play(self, player: Player):
        self.curr_hand = player.hand.card_list
        valid_plays = self.get_valid_plays()
        if player.is_ai:
            play = self.get_ai_play(valid_plays, player.hand)
        else:
            play = self.get_user_play(player.hand.get_all_valid_cards(self.is_valid_play), player.hand)
        self.pot.add_card(play)
        player.hand.rem_card(play)
        CardLib.gui.redraw()
        if not self.spades_broken:
            if play.suit == CardLib.SPADE:
                self.spades_broken = True
                print("Spades Broken:")
        return player

    def is_valid_play(self, card):
        cards = self.get_valid_plays()
        return card in cards

    def get_valid_plays(self) -> Hand:
        cards = []
        if self.pot.num_cards_left() == 0:
            if self.spades_broken:
                [cards.append(card) for card in self.curr_hand]
            else:
                [cards.append(card) for card in [card for card in self.curr_hand if card.suit != CardLib.SPADE]]
        else:
            led_card = self.pot.get_card_at(0)
            [cards.append(card) for card in [card for card in self.curr_hand if card.suit == led_card.suit]]
            if len(cards) == 0:
                [cards.append(card) for card in self.curr_hand]
        return cards

    def get_user_play(self, valid_plays, hand):
        valid_play = False
        while not valid_play:
            play = CardLib.gui.get_gui_user_input(valid_plays)
            valid_play = True
            return play

    def get_ai_play(self, valid_plays: CardList, hand: Hand) -> Card:
        if len(valid_plays) == 1:
            return valid_plays[0]
        if self.pot:
            card_to_beat = self.get_winning_card()
        else:
            card_to_beat = None
        ratios = self.winning_ratios(card_to_beat, valid_plays, hand)
        return self.get_choice(valid_plays, ratios)

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
        ratios = [self.get_ratio(card, possible_losses, card_to_beat) for card in plays]
        remaining_plays = (self.player_count - self.pot.num_cards_left()) - 1
        output = []
        for ratio in ratios:
            try:
                output.append(float(ratio ** remaining_plays))
            except InvalidOperation:
                output.append(0)
        return output

    def get_ratio(self, card: Card, cards: CardList, card_to_beat: Card) -> Decimal:
        losses = loss_count(card, cards, card_to_beat)
        total = Decimal(cards.num_cards_left())
        print(total, losses)
        if total == 0 and losses == 0:
            return Decimal(0)
        else:
            return (total - losses) / total

    def get_choice(self, plays: [Card], ratios: [float]):
        non_zeros = [num for num in ratios if num != 0]
        if non_zeros:
            if len(set(non_zeros)) == 1:
                good_plays = []
                for i, card in enumerate(plays):
                    if ratios[i] != 0:
                        good_plays.append(card)
                return min(good_plays)
            else:
                return random.choices(plays, weights=ratios)[0]
        else:
            return min(plays)

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
