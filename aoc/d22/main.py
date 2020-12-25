from typing import IO
from collections import deque
import re
import copy
import itertools
import numpy as np


def parse_file(input_file):
    '''parse the file and return a stack of each thing. this is quite
    because it assumes there are only 2 players and is kind of messy...'''
    for line in input_file.readlines():
        re_player = re.compile(r"(Player)\s([1-2])")
        player_str = re_player.match(line)
        if player_str is not None:
            groups = player_str.groups()
            if groups[1] == '1':
                current_player = deque()
            else:
                player_1 = current_player
                current_player = deque()
        elif line == '\n':
            continue
        else:
            current_player.append(int(line.strip()))
    player_2 = current_player
    return player_1, player_2


def play_round(player_1, player_2, card_1, card_2):
    '''play a round'''
    if card_1 > card_2:
        player_1.append(card_1)
        player_1.append(card_2)
    else:
        player_2.append(card_2)
        player_2.append(card_1)
    return player_1, player_2


def calc_winner_number(winner):
    '''calculate the winner's score'''
    mult = list(range(len(winner), 0, -1))
    return np.dot(mult, winner)


def p_1(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''play a game
    3400 too low'''
    player_1, player_2 = parse_file(input_file)

    while player_1 and player_2:
        card_1, card_2 = player_1.popleft(), player_2.popleft()
        play_round(player_1, player_2, card_1, card_2)
    if len(player_1) == 0:
        winner = player_2
    else:
        winner = player_1
    return calc_winner_number(winner)

def play_game_wrapper(player_1, player_2):
    '''wrapper for the recursion?'''
    hands = []
    finished = False
    while player_1 and player_2:
        if [player_1, player_2] in hands:
            finished = True
            return 1, player_1, finished
        hands.append([copy.copy(player_1), copy.copy(player_2)])
        player_1, player_2 = play_game(player_1, player_2)
    if len(player_1) == 0:
        return 2, player_2, finished
    return 1, player_1, finished

def play_game(player_1, player_2):
    '''play the recursive game....'''
    card_1, card_2 = player_1.popleft(), player_2.popleft()
    if card_1 > len(player_1) or card_2 > len(player_2):
        player_1, player_2 = play_round(player_1, player_2, card_1, card_2)
        return player_1, player_2
    new_player_1 = deque(list(itertools.islice(player_1, 0, card_1)))
    new_player_2 = deque(list(itertools.islice(player_2, 0, card_2)))
    winner, _ , _ = \
        play_game_wrapper(copy.copy(new_player_1), copy.copy(new_player_2))
    if winner == 1:
        return player_1 + deque([card_1, card_2]), player_2
    return player_1, player_2 + deque([card_2, card_1])

def p_2(input_file: IO,
        debug=False):  # pylint: disable=unused-argument
    '''play the recursive game...
    24257 is too low'''
    player_1, player_2 = parse_file(input_file)
    finished = False
    while player_1 and player_2 and not finished:
        _, winning_deck, finished = play_game_wrapper(player_1, player_2)
    return calc_winner_number(winning_deck)
