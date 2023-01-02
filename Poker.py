import time
import random

import DisplayMode
from constant import *
import setting


class Poker:

    _card_set = []
    _mixed = False
    _turtle_got = False
    _distributed = False

    def __init__(self, show_process=True):
        while len(self._card_set) != TOTAL_CARDS:
            randnum = random.randint(0, TOTAL_CARDS - 1)
            if not self._check_if_exist(randnum):
                self._card_set.append(randnum)

        if show_process:
            # show the process of mixing poker
            print("")
            mixtime = random.randint(4, 7)
            for x in range(0, mixtime):
                if setting.Waiting:
                    time.sleep(0.32)
                print("\t   Mixing Poker Cards...")
            print("")

        self._mixed = True

    #   _check_if_exist -- Check if the poker is already exist in Poker Set (Use for MixingPoker)
    #   Return True if the card already exist
    #   Input Format:   (int, GameSet.PokerSet)
    #   Return Format:  True / False
    def _check_if_exist(self, index):
        if index in self._card_set:
            return True
        return False

    def get_turtle_card(self):
        if self._turtle_got:
            return
        turtle_card = self._card_set.pop(random.randint(0, TOTAL_CARDS - 1))
        self._turtle_got = True
        return turtle_card

    #   distribute_poker -- Distribute the poker card
    #   Input format:   number of player
    #   Return format:  None
    def distribute_poker(self, num_of_player):
        if self._distributed:
            return
        # Check if the card already distributed
        distributed_card = []

        # Temp list for every player - temphands
        players_cards = []
        for j in range(0, num_of_player):
            players_cards.append([])

        # Distribute all card in player list
        max_num_cards_per_player = 10
        index = 0

        while index < len(self._card_set):
            playerposition = random.randint(0, num_of_player - 1)
            if self._card_set[index] not in distributed_card and len(
                players_cards[playerposition]
            ) < max(max_num_cards_per_player, TOTAL_CARDS // num_of_player + 1):
                players_cards[playerposition].append(self._card_set[index])
                distributed_card.append(self._card_set[index])
                index += 1

        self._distributed = True
        return players_cards


# ================== Function to handle poker cards ======================================

#   convert_index_to_card -- Convert random number into Card with type and number
#   Input Format:   int
#   Return Format:  list[int,int]
#   Example: 0 => [1,0] / 1 => [1,1]
def convert_index_to_card(index_number):
    card_in_num = []
    card_type = int(index_number / 13)
    card_num = int(index_number % 13)
    # if this is Spades
    if card_type == 0:
        card_in_num.append(1)
    # if this is Hearts
    elif card_type == 1:
        card_in_num.append(2)
    # if this is Clubs
    elif card_type == 2:
        card_in_num.append(3)
    # if this is Diamonds
    elif card_type == 3:
        card_in_num.append(4)

    card_in_num.append(card_num)
    return card_in_num


#   convert_card_to_index -- Convert Card into Index
#   Input Format:   list[int,int]
#   Return Format:  int
#   Example: [1(Spade),0(Ace)] => 0, [1(Spade),4] => 4
def convert_card_to_index(card):
    card_num = int(card[1])
    card_type = int(card[0])
    card_index = 0
    # if this is Spades
    if card_type == 1:
        card_index = 0 * 13
    # if this is Hearts
    elif card_type == 2:
        card_index = 1 * 13
    # if this is Clubs
    elif card_type == 3:
        card_index = 2 * 13
    # if this is Diamonds
    elif card_type == 4:
        card_index = 3 * 13

    card_index += card_num
    return card_index


#   convert_indexs_to_hands -- Convert cards into Hand with type and number
#   Input a list of number and Return with 2D List
#   Input format:   list of int (e.g. [3,4,23,6,18...])
#   Return format:  list of [int,int]
def convert_indices_to_hands(index_list):
    hand_list = []
    for x in range(0, len(index_list)):
        convert_card = convert_index_to_card(index_list[x])
        hand_list.append(convert_card)
    return hand_list


#   convert_hands_to_lengthy_simply_hands -- Convert Hand with detailed Hand
#   Input a 2D list of number and Return with 2D List with card type and number
#   Input format:   list of [int,int]
#   Return format:  list of [str,str]
def convert_hands_to_lengthy_simply_hands(original_hand, display_mode):
    lengthy_hands = []
    for x in range(0, len(original_hand)):
        modified_hand = []
        modified_hand.append(TYPE_DICT[original_hand[x][0]])
        if display_mode == DisplayMode.DisplayMode.LENGTHY:
            modified_hand.append(NUM_FULL_DICT[original_hand[x][1]])
        elif display_mode == DisplayMode.DisplayMode.SIMPLY:
            modified_hand.append(NUM_SHORT_DICT[original_hand[x][1]])
        lengthy_hands.append(modified_hand)
    return lengthy_hands


#   convert_lengthy_simply_hand_to_index -- Convert Cards to Index
#   Input format:   [str,str]
#   Return format:  int
def convert_lengthy_simply_hand_to_index(source_cards):
    if source_cards[0] == "Spades":
        index = (1 - 1) * 13
    elif source_cards[0] == "Hearts":
        index = (2 - 1) * 13
    elif source_cards[0] == "Clubs":
        index = (3 - 1) * 13
    elif source_cards[0] == "Diamonds":
        index = (4 - 1) * 13

    if source_cards[1] == "A" or source_cards[1] == "Ace":
        index += 0
    elif source_cards[1] == "K" or source_cards[1] == "King":
        index += 12
    elif source_cards[1] == "Q" or source_cards[1] == "Queen":
        index += 11
    elif source_cards[1] == "J" or source_cards[1] == "Jack":
        index += 10
    else:
        index += int(source_cards[1]) - 1
    return index


#   convert_lengthy_simply_hands_to_indexs -- Convert Detailed Hands into Hands with Index
#   Input format:   list of [str,str]
#   Return format:  list iof int
def convert_lengthy_simply_hands_to_indices(source_hands):
    new_hands = []
    for x in range(len(source_hands)):
        new_hands.append(convert_lengthy_simply_hand_to_index(source_hands[x]))
    return new_hands


#   print_lengthy_simply_hands -- print the cards of your hand
#   Input a 2D list (hand) and print out the hands
#   Input format:   list of [str,str]
#   Return format:  None
def print_lengthy_simply_hands(hands):
    for x in range(0, len(hands) - 1):
        if hands[x][0] == hands[x + 1][0]:
            print(hands[x], end="")
        else:
            print(hands[x])
    print(hands[len(hands) - 1])


#   eliminate_pair_with_indexs -- Eliminate the pair with the list with card index
#   Input format:   list[int]
#   Return format:  list[str ... str][str,str]
# def eliminate_pair_with_indexs(index_list, display_mode):
#     return eliminate_pair_with_lengthy_simply_hands(
#         convert_hands_to_lengthy_simply_hands(convert_indices_to_hands(index_list)),
#         display_mode,
#     )


#   Eliminate the pair with input of Detailed Hands
#   Input format:   list of [str,str]
#   Return format:  list of [str,str]
# def eliminate_pair_with_lengthy_simply_hands(detailed_hands, display_mode):
#     if display_mode == DisplayMode.DisplayMode.SIMPLY:
#         dict_standard = NUM_SHORT_DICT.copy()
#     elif display_mode == DisplayMode.DisplayMode.LENGTHY:
#         dict_standard = NUM_FULL_DICT.copy()
#     temp_hands = []
#     count = []
#     for i in range(0, len(dict_standard)):
#         count.append(0)
#     for x in range(0, len(detailed_hands)):
#         for y in range(0, len(dict_standard)):
#             if detailed_hands[x][1] == dict_standard[y]:
#                 count[y] = count[y] + 1

#     for u in range(0, len(dict_standard)):
#         if count[u] % 2 != 0:
#             target = dict_standard[u]
#             if count[u] == 1:
#                 for v in range(0, len(detailed_hands)):
#                     if detailed_hands[v][1] == target:
#                         temp_hands.append(detailed_hands[v])
#             elif count[u] == 3:
#                 appeartime = 0
#                 for s in range(0, len(detailed_hands)):
#                     if detailed_hands[s][1] == target and appeartime == 2:
#                         temp_hands.append(detailed_hands[s])
#                     elif detailed_hands[s][1] == target and appeartime < 2:
#                         appeartime = appeartime + 1
#     return temp_hands


def eliminate_pair_by_indice(index_list):
    player_card_list = []
    for i in range(13):
        player_card_list.append([])

    random.shuffle(index_list)
    for index in index_list:
        player_card_list[index % 13].append(index)
        if len(player_card_list[index % 13]) == 2:
            player_card_list[index % 13].clear()

    final_index_list = [
        each_card for card_num in player_card_list for each_card in card_num
    ]
    return final_index_list

