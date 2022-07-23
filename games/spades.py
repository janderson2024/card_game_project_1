import CardLib


WINNING_SCORE = 300


def start_game():
    player_list, player_count, scores = setup_game()
    while is_no_winner(scores):
        player_list = setup_round(player_list, player_count)
        bids = get_bids(player_list)
        for player in player_list:
            print(player.hand)
        print(bids)
        scores[0] = 300


def setup_game():
    player_count, none = CardLib.get_user_input(["4", "6"], "How many players?")
    player_list = [CardLib.Player("Player")]
    scores = [0]

    for num in range(1, int(player_count)):
        player_list.append(CardLib.Player("AI #" + str(num), is_ai=True))
        scores.append(0)

    return player_list, int(player_count), scores


def is_no_winner(scores):
    return [score for score in scores if score >= WINNING_SCORE] == []


def setup_round(player_list, player_count):
    pack = CardLib.Draw([])
    if player_count == 4:
        CardLib.fill_deck_standard_52(pack, ace_high=True)
    elif player_count == 6:
        CardLib.fill_deck_standard_54(pack, ace_high=True)
    pack.shuffle()
    pack, player_list = CardLib.deal_to_players(pack, player_list, pack.num_cards_left() // player_count)
    [player.hand.sort_suit() for player in player_list]
    return player_list


def get_bids(player_list):
    return [get_bid(player) for player in player_list]


def get_bid(player):
    hand = player.hand
    if player.is_ai:
        strengths = [get_strength(card) for card in hand.card_list]
        strength = int(sum(strengths) // 1)
        if strength < 1:
            strength = 1
        return strength
    else:
        return int(CardLib.get_user_input([str(num + 1) for num in range(hand.num_cards_left())],
                                      str(hand) + "\nHow many tricks would you like to bid?")[0])


def get_strength(card):
    if card.value >= 14:
        return 1
    elif card.value >= 12:
        return .5
    elif card.suit_text == "spades":
        return .25
    else:
        return 0



