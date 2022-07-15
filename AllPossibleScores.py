import itertools

def CalcAllScoresFaster(rules, cards):
    cards_values = [rules[card] for card in cards]
    
    score = sum([value for value in cards_values if type(value) is int])
    poss_perms = [value for value in cards_values if type(value) is tuple]

    result = [score + sum(combo) for combo in itertools.product(*poss_perms)]

    return list(set(result))


if __name__ == '__main__':    

    #based on the 1-13 value for the cards, and the rules following blackjack rules.
    #gives a full list of all the possible score permutations

    test_cards = [1, 11]

    rules = {
        1: (1,11),
        2: (2),
        3: (3),
        4: (4),
        5: (5),
        6: (6),
        7: (7),
        8: (8),
        9: (9),
        10: (10),
        11: (10),
        12: (10),
        13: (10)
    }

    print("All Scores: ", CalcAllScoresFaster(rules, test_cards))