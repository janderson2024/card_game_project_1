import CardLib
from random import randint

from CardLib.cardlists import CardList
from CardLib.cardlists import Hand
from CardLib import Card, Player

WINNING_SCORE = 100


def start_game():
    player_list, player_count, scores = setup_game()
    while is_no_winner(scores):
        spades_broken = False
        player_list = setup_hand(player_list, player_count)
        bids = get_bids(player_list)
        print("\n\n\n-----Bids----: " + str(bids))
        leader = bids.index(max(bids))
        tricks = do_hand(leader, player_list, player_count, spades_broken)
        print("-----Bids----: " + str(bids))
        print("----Tricks---: " + str(tricks))
        new_scores = get_scores(bids, tricks)
        scores = [old + new for old, new in zip(scores, new_scores)]
        print("----Scores---: " + str(scores))


def setup_game() -> ([Player], int, [int]):
    player_count, none = CardLib.get_user_input(["4", "6"], "How many players?")
    player_list = [CardLib.Player("Player")]
    scores = [0]

    for num in range(1, int(player_count)):
        player_list.append(CardLib.Player("AI #" + str(num), is_ai=True))
        scores.append(0)

    return player_list, int(player_count), scores


def is_no_winner(scores: [int]) -> bool:
    return [score for score in scores if score >= WINNING_SCORE] == []


def setup_hand(player_list: [Player], player_count: int) -> [Player]:
    pack = CardLib.Draw([])
    if player_count == 4:
        CardLib.fill_deck_standard_52(pack, ace_high=True)
    elif player_count == 6:
        CardLib.fill_deck_standard_54(pack, ace_high=True)
        pack.get_card_at(-1).suit = CardLib.SPADE
        pack.get_card_at(-2).suit = CardLib.SPADE
    pack.shuffle()
    pack, player_list = CardLib.deal_to_players(pack, player_list, pack.num_cards_left() // player_count)
    [player.hand.sort_by_suit() for player in player_list]
    return player_list


def get_bids(player_list: [Player]) -> [int]:
    return [get_bid(player) for player in player_list]


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


def do_hand(leader: int, player_list: [Player], player_count: int, spades_broken: bool) -> [int]:
    tricks = [0 for _ in range(player_count)]
    while player_list[0].hand.num_cards_left() > 0:
        print("----Tricks---: " + str(tricks))
        leader, player_list, spades_broken = do_round(leader, player_list, player_count, spades_broken)
        tricks[leader] += 1
    return tricks


def do_round(leader: int, player_list: [Player], player_count: int, spades_broken: bool) -> (int, [Player], bool):
    pot = CardLib.CardList([])
    while pot.num_cards_left() < player_count:
        pot, player_list[leader], spades_broken = get_play(pot, player_list[leader], spades_broken)
        print("---Player " + str(leader + 1) + "--: Played " + str(pot.get_card_at(-1)))
        leader = next_player(leader, player_count)
    winning_card = get_winning_card(pot.card_list)
    leader = pot.get_card_list().index(winning_card) + leader
    if leader >= player_count:
        leader -= player_count
    print("---Player " + str(leader + 1) + "--: Takes the trick ")
    return leader, player_list, spades_broken


def get_play(pot: CardList, player: Player, spades_broken: bool):
    valid_plays = get_valid_plays(pot, player.hand, spades_broken)
    if player.is_ai:
        play = get_ai_play(pot, valid_plays)
    else:
        play = valid_plays.get_card_at(
            int(CardLib.get_user_input([str(num + 1) for num in range(valid_plays.num_cards_left())],
                                       "-----Pot-----: " + str(pot) + "\n" +
                                       "-----Hand----: " + str(player.hand) + "\n" +
                                       "-Valid Plays-: " + str(valid_plays))[0]) - 1)
    pot.add_card(play)
    player.hand.rem_card(play)
    if not spades_broken:
        if play.suit == CardLib.SPADE:
            spades_broken = True
            print("Spades Broken:")
    return pot, player, spades_broken


def get_valid_plays(pot: CardList, hand: Hand, spades_broken: bool) -> Hand:
    cards = CardLib.Hand([])
    if pot.num_cards_left() == 0:
        if spades_broken:
            cards.add_cards(hand.get_card_list())
        else:
            cards.add_cards([card for card in hand.card_list if card.suit != CardLib.SPADE])
    else:
        led_card = pot.get_card_at(0)
        cards.add_cards([card for card in hand.card_list if card.suit == led_card.suit])
        if cards.num_cards_left() == 0:
            cards.add_cards(hand.get_card_list())
    return cards


def get_ai_play(pot: CardList, valid_plays: CardList) -> Card:
    return valid_plays.get_card_at(randint(0, valid_plays.num_cards_left() - 1))


def next_player(leader: int, player_count: int) -> int:
    if leader >= player_count - 1:
        return 0
    else:
        return leader + 1


def get_winning_card(card_list):
    lead_suit = card_list[0].suit
    spades = [card for card in card_list if card.suit == CardLib.SPADE or card.suit == CardLib.JOKER]
    if len(spades) == 0:
        return CardLib.get_highest_card(
            [card for card in card_list if card.suit == lead_suit])
    else:
        return CardLib.get_highest_card(spades)


def get_scores(bids: [int], tricks: [int]) -> [int]:
    return [calc_score(bid, trick) for (bid, trick) in zip(bids, tricks)]


def calc_score(bid: int, trick: int) -> int:
    if bid <= trick:
        return bid * 10 + (trick - bid)
    else:
        return 0
